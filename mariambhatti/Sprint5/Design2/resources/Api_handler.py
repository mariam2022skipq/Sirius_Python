import json
import os
import boto3
from datetime import datetime

# https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
db = boto3.resource("dynamodb", region_name="us-east-2")
# Get key value of the table
dbnameTable = os.environ["EventTable"]
table = db.Table(dbnameTable)

URL=[]
def lambda_handler(event, context):
     
    Method = event["httpMethod"]
    val=event["body"]

    if Method == "POST":
        #creating a variable to parse my event in the given form
        dict_mariam = [{
                  "event1":{"attr1": val }
                  
              }]
        val=dict_mariam[0]['event1']['attr1']
        timestamp=event["requestContext"]["requestTime"]
        #timestamp = datetime.now().isoformat()

        # https://dynobase.dev/dynamodb-python-with-boto3/#put-item
        response=table.put_item(
        Item={
                "Timestamp": timestamp,
                "val": val,
               })
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps('URL Added Successfully')
        }



    elif Method == "GET":
        #https://dynobase.dev/dynamodb-python-with-boto3/#scan
        #Getting all the items from dynamo db

        response = table.scan()
        list_items = response['Items']
        array=[]
        #Appending item values : TimeStamp and Values  in an array
        #I have given partition key as Timestamp
        for i in range(len(list_items)):
            array.append([list_items[i]["Timestamp"], list_items[i]["val"]])

        #sorting the array to get the latest elements
        latest_items=sorted(array, reverse=True)

        #Returning these lines in reuturn of correct response when Get operation is done successfully
        if len(latest_items)<=10:
            return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(latest_items),
        }
            
        else:
             return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': json.dumps(latest_items),
        }

            

       
   