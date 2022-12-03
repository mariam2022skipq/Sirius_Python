import datetime
import urllib3
import boto3
import json
import logging
import os
from custom_encoder import customEncoder
from cloudwatch_putData import AWSCloudWatch
import constants as constants
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#URL_TO_BE_MONITORED =["skipq.org","youtube.com","google.com","amazon.com"]
url_list=[]
values=[]
def lambda_handler(event, context):
    tablename = os.getenv("CRUD_tablewebHealth2")
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(tablename)

    #https://dynobase.dev/dynamodb-python-with-boto3/
    response = table.scan()
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    for i in range(len(data)):
        url_list.extend(data[i]["URL"])

    #creating a cloudwatch object
    cloudwatch_object=AWSCloudWatch()
    #we have to get the availability and latency of each of the URLs by passing cloudwath_metric_data
    for url in url_list:
        dimensions=[{'Name':'URL', 'Value':url}]
        availability=getAvail(url);
        latency=getLatency(url);
        cloudwatch_object.cloudwatch_metric_data(constants.namespace, constants.AvailabilityMetric,dimensions,availability)
        cloudwatch_object.cloudwatch_metric_data(constants.namespace, constants.LatencyMetric,dimensions,latency)
        values.update({"availability"+str(url):availability, "latency" + str(url):latency})
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


