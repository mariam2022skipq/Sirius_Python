import json
import os
import boto3

# https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
db = boto3.resource('dynamodb', region_name='us-east-2')
        
#https://www.geeksforgeeks.org/python-os-getenv-method/
# Extracting the value of table using environment variables
dbnameTable=os.getenv("ArgTable")
table=db.Table(dbnameTable)

ARG=[]
def lambda_handler(event, context):
    # Get the method
    method=event["httpMethod"]
    # Get the url
    arg=event["body"]

    # Perform CRUD operation if method matches
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html?highlight=dynamodb
    if method=="POST":
        response = table.put_item(
                            Item={ 
                                "ARG":arg
                            }
                        )
        # Return these lines to be shown in API when doing CRUD operation
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'Argument value Added Successfully'
        }
        
    
    if method=="GET":
        response = table.scan()
        data=response["Items"]
        for urls in data:
            ARG.append(urls['ARG'])
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': ARG
        }

    
    if method=="PATCH":
        response=table.update_item(
                            Key={
                                "ARG":arg
                            },
                            UpdateExpression='SET ARG = :url11',
                            ExpressionAttributeValues={
                                                    ':url1': arg
                                                    }
                            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'argument Updated Successfully'
        }
    
    if method=="DELETE":
        response=table.delete_item(
                                Key={
                                    "ARG":arg
                                    }
                            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'Argument Deleted Successfully from table'
        }
        