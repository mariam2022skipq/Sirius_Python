import datetime
import urllib3
import boto3
from cloudwatch_putData import AWSCloudWatch
import constants as constants

URL_TO_BE_MONITORED =["skipq.org","youtube.com","google.com","amazon.com"]


def lambda_handler(event, context):
    #creating a cloudwatch object
    cloudwatch_object=AWSCloudWatch()
    values=dict()
    #looping through the UR_TO_BE_MONITORED list as we have 4 URLS whose health have to be monitored
    #we have to get the availability and latency of each of the URLs by passing cloudwath_metric_data
    for url in constants.URL_TO_BE_MONITORED:
        availability=getAvail(url);
        latency=getLatency(url);
        dimensions=[{'Name':'url', 'Value':url}]
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


