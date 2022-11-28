import boto3
import os

def lambda_handler(event, context):
    client =boto3.resource('dynamodb', region_name='us-east-2')
    #get the key of the table
    dbTable = os.environ['AlarmTable']
    table=client.Table(dbTable)
    #extracting message ID and timestamp from the JSON file ; parsing the event data
    message_id = event["Records"][0]["Sns"]["MessageId"]
    timestamp = event["Records"][0]["Sns"]["Timestamp"]
    #passing the event data after parsing to the DB_putdata table
    #in the put_data_in_dynamoDB function inside dynamo_data class
    response=table.put_item(Item={"id": message_id, "Timestamp": timestamp})

