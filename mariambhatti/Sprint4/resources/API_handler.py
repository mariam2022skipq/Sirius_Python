import json
import os
import boto3

# https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
db = boto3.resource('dynamodb', region_name='us-east-2')
        
#https://www.geeksforgeeks.org/python-os-getenv-method/
# Get key value of the table
dbTable=os.getenv("CRUD_URL_Table")
table=db.Table(dbTable)

def lambda_handler(event, context):
    httpmethod=event["httpMethod"]
    url=event["body"]
    if httpmethod=="POST":
        response = table.put_item(
            Item={ "url":url},
        )
        print("POST")
    
    if httpmethod=="GET":
        print("GET method")
    
    