import boto3
import os

def lambda_handler(event, context):
    #extracting message ID and timestamp from JSOn file
    client = boto3.resource('dynamodb',region_name = 'us-east-2')
    dbtable=os.environ['Alarmtable']
    table = client.Table(dbtable)
    message_id = event["Records"][0]["Sns"]["MessageId"]
    timestamp = event["Records"][0]["Sns"]["Timestamp"]
    response = table.put_item(Item={'id':message_id,'Timestamp':timestamp})






