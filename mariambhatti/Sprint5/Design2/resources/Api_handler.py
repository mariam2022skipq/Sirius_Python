import json
import os
import boto3
from datetime import datetime


def lambda_handler(event, context):
        # https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
    db = boto3.resource("dynamodb", region_name="us-east-2")
    
    # https://www.geeksforgeeks.org/python-os-getenv-method/
    # Get key value of the table
    dbnameTable = os.environ["EventTable"]
    table = db.Table(dbnameTable)
    Method = event["httpMethod"]

    if Method == "POST":
        #myevent =json.loads(event["body"]) # json.loads()  converts  valid JSONstring file into json or python Dictionary.
        #val = myevent[0]["event1"]["attr1"] # slicing : fetching events1 and attr1
        val=event["body"]
        timestamp=event["requestContext"]["requestTime"]
        #timestamp = datetime.now().isoformat()

            # https://dynobase.dev/dynamodb-python-with-boto3/#put-item
        response=table.put_item(
        Item={
                "Timestamp": timestamp,
                "val": val,
               })
        return {
            "body":"Value Added"
        }



    elif Method == "GET":
        response = table.scan()
        list_items = response['Items']
        array=[]
        for i in range(len(list_items)):
            array.append([list_items[i]["Timestamp"], list_items[i]["val"]])
        latest_items=sorted(array, reverse=True)
        if len(latest_items)<=10:
            print(latest_items)
        else:
            print(latest_items[0:10])
        return {"body": f"{latest_items[:10]}"}

       
    # response = {
    #         "statusCode": 200,
    #         "body": body,
    #         "isBase64Encoded": False
    #     }
    # return response