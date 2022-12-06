import os
import boto3
import urllib3
import datetime
from cloudwatch_putdata import AWSCloudWatch
import constants as constants

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
dynamodb=boto3.resource('dynamodb',region_name='us-east-2')
table_name = os.environ['URLTable']
table = dynamodb.Table(table_name)

#url list for stroing values from URL table
URL =[]
#for storing values 
values=[]

def lambda_handler(event, context):
    
    topicname=os.environ["topicname"]
    AlarmActions = ["arn:aws:sns:us-east-2:315997497220:{topicname}".format(topicname=topicname)]
    
    #creating a cloudwatch object
    cloudwatch_object = AWSCloudWatch()
    
    """ Executing functions to fetch website active status and latency """
    response = table.scan()
    lists=response["Items"]
    for l in lists:
        URL.append(l["URL"])
        
    
    for i in URL:
        dimensions = [{ 'Name': 'URL', 'Value': i}]
        availability = getAvail(i)
        latency = getLatency(i)
        

        """ Sending data to CloudWatch """
        # Availability Metric   
        cloudwatch_object.cloudwatch_metric_data(constants.nameSpace, constants.AvailabilityMetric, dimensions, availability )
        cloudwatch_object.cloudWatch_metric_alarm("Availability_website" + str(i),
        AlarmActions,constants.AvailabilityMetric,constants.nameSpace,dimensions,1,"LessThanThreshold")
        
        # Latency Metric
        cloudwatch_object.cloudwatch_metric_data(constants.nameSpace, constants.LatencyMetric, dimensions, latency )
        cloudwatch_object.cloudWatch_metric_alarm("Latency_of_website" + str(i),
        AlarmActions,constants.LatencyMetric,constants.nameSpace,dimensions,0.3,"GreaterThanThreshold")
        
        values.append({"availability of " + str(i): availability,"latency of " + str(i): latency})
        
            
    return values

def getAvail(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    if response.status == 200:
        return 1.0
    else:
        return 0.0

def getLatency(url):
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET", url)
    end = datetime.datetime.now()
    delta = end - start             # Take time difference
    latencySec = round(delta.microseconds * .000001, 6)
    return latencySec