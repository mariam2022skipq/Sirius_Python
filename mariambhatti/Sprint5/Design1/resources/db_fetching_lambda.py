import urllib3
import datetime
from cloudwatch_putdata import AWSCloudWatch
import constants as constants
import boto3
import os

# https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
db = boto3.resource('dynamodb', region_name='us-east-2')

# https://www.geeksforgeeks.org/python-os-environ-object/
# Get key value of the table
dbnameTable=os.environ["ArgTable"]
table=db.Table(dbnameTable)
# Get topic of sns
snsTopic=os.environ["snsTopic"]
AlarmActions = ["arn:aws:sns:us-east-2:315997497220:{snsTopic}".format(snsTopic=snsTopic)]

#array for storing websites
ARG =[]
values=[]


def lambda_handler(event, context):
    # CloudWatchAWS Object
    cloudWatch_Object=AWSCloudWatch()

    #values extraction from table using scan
    response = table.scan()
    lists=response["Items"]
    for i in lists:
        ARG.append(i['ARG'])
    i=1
    for j in ARG:
        
        dimensions=[{'Name': 'ARG', 'Value': j} ]
        n=int(j)
        
        #Sending argument metrics to cloudwatch for alarms
        cloudWatch_Object.cloudWatch_metrics(constants.namespace,constants.AvailabiltyMetric, dimensions, n)
        
        cloudWatch_Object.cloudWatch_alarms("Mariam-Argument of "+str(i),
        AlarmActions,constants.AvailabiltyMetric,constants.namespace,dimensions,10,"GreaterThanThreshold")

        values.append({"ARG "+str(i)+": ":n})
        i+=1
        
        
    return values