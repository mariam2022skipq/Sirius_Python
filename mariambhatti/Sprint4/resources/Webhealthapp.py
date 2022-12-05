import datetime
import urllib3
import boto3
import json
import logging
import os

from custom_encoder import customEncoder
import constants as constants
from resources.cloudwatch_putalarm import cloudwatchPutAlarm
from resources.cloudwatch_putmetric import cloudwatchPutMetric
logger = logging.getLogger()

logger.setLevel(logging.INFO)

topicname = os.getenv("topicName")

AvailabilityMetricName = 'URL_AVAILABILITY'
LatencyMetricName = 'URL_LATENCY'
namespace = 'MariamBhattisprint2Namespace'
AvailabilitycomparisonOperator = 'LessThanThreshold'
latencycomparisonOperator = 'GreaterThanThreshold'
AvailabilityThreshold = 1
LatencyThreshold = 0.6
AlarmActions = ["arn:aws:sns:us-east-2:315997497220:{topicname}".format(topicname=topicname)]


#URL_TO_BE_MONITORED =["skipq.org","youtube.com","google.com","amazon.com"]
url_list=[]
values=[]
tablename = os.getenv("CRUD_tablewebHealth2")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)

def lambda_handler(event, context):

    #https://dynobase.dev/dynamodb-python-with-boto3/
    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    for i in range(len(data)):
        url_list.append(data[i]["web_URL"])

    #creating a cloudwatch object
    cw = cloudwatchPutMetric()
    cwa = cloudwatchPutAlarm()
    
    #we have to get the availability and latency of each of the URLs by passing cloudwath_metric_data
    for url in url_list:
        dimensions=[{'Name':'url', 'Value':url}]
        AvailabilityAlarmName = "Mariam_Availability_{web_url}".format(web_url=url)
        LatencyAlarmName = "Yousaf_Latency_{web_url}".format(web_url=url)
        #AlarmDescription = "Alarm_of_{web_url}".format(web_url=url)
        
                
        avail =  getAvail(url)
        cw.putData(constants.namespace, constants.AvailabilityMetric, dimensions, avail)
        
        cwa.putAlarm(AvailabilityAlarmName, AlarmActions, AvailabilityMetricName,
        namespace, dimensions, AvailabilitycomparisonOperator,AvailabilityThreshold)

        
        
        #get the latency of website
        lat  = getLatency(url)
        cw.putData(constants.namespace, constants.LatencyMetric, dimensions, lat)
        
        cwa.putAlarm(LatencyAlarmName, AlarmActions,LatencyMetricName,
        namespace,dimensions,latencycomparisonOperator,LatencyThreshold)


        
        
        # update values of latency and availablity to dictionary.
        values.append(({"website": url , "availability ": avail, "latency (s)" : lat}))

        

        
        
        #return availability and latency of website.
        
    return values



def getAvail(url):
    http=urllib3.PoolManager()
    response=http.request("GET",url)
    if response.status==200:
        return 1.0
    else:
        return 0.0
def getLatency(url):
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET",url)
    end=datetime.datetime.now()
    delta=end-start
    latencySec=round(delta.microseconds* .000001,6)
    return latencySec


