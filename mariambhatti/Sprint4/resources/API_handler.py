from unittest import result
from urllib import response
import boto3
import json
import logging
import os

#Access table through lambda function
tablename = os.getenv("URLTable")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)

"""CRUD API for saving the url of websites"""
#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
URL=[]
def lambda_handler(event, context):
    # Get the method
    httpmethod=event["httpMethod"]
    # Get the url
    url=event["body"]

    # Perform CRUD operation if method matches
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html?highlight=dynamodb
    if httpmethod=="POST":
        response = table.put_item(
                            Item={ 
                                "url":url
                            }
                        )
        # Return these lines to be shown in API when doing CRUD operation
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Added Successfully'
        }
        
    
    if httpmethod=="GET":
        response = table.scan()
        data=response["Items"]
        for urls in data:
            URL.append(urls['url'])
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': URL
        }

    
    
    if httpmethod=="DELETE":
        response=table.delete_item(
                                Key={
                                    "url":url
                                    }
                            )
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Deleted Successfully'
        }
        
    
    