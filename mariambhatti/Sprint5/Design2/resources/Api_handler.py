import json
import os
import boto3
from datetime import datetime

# https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
db = boto3.resource("dynamodb", region_name="us-east-2")

# https://www.geeksforgeeks.org/python-os-getenv-method/
# Get key value of the table
dbnameTable = os.environ["EventTable"]
table = db.Table(dbnameTable)


def lambda_handler(event, context):
    # Get the method
    httpmethod = event["httpMethod"]
    # Get the url
    body = event["body"]
    # taking request time from event
    requestTime = event["requestContext"]["requestTime"]
    # taking current date time
    now = datetime.now()
    date_ = now.isoformat()

    # adding attr1 and request time in our api table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Table.put_item
    if httpmethod == "POST":

        key = {"arg": body, "requestTime": date_}

        response = table.put_item(
            Item=key,
        )

        if response:
            return json_response(
                {"message": "Entered the value in the table successfully"}
            )
        else:
            return json_response({"message": "Invalid Response"})

    # Reading the 10 latest events from table
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan

    else:
        response = table.scan(Limit=10)["Items"]

        if response:
            return json_response(response)
        else:
            return json_response({"message": "The table is empty"})


# Defining the json response method for returning response in json format
def json_response(res):
    return {
        "statusCode": 200,
        "body": json.dumps(res),
        "headers": {"Content-Type": "application/json"},
    }
