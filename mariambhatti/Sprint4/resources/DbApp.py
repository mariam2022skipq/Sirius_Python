import boto3
import os

def lambda_handler(event,context):
    # Get the service resource.
    client = boto3.resource('dynamodb',region_name = 'us-east-2')
    #get the key of the table
    dbTable=os.environ['AlarmTable']
    table = client.Table(dbTable)
    message=event["Records"][0]["Sns"]["MessageId"]
    time=event["Records"][0]["Sns"]["Timestamp"]
    response = table.put_item(Item={'id':message,'Timestamp':time})

    
     

   
   
    









