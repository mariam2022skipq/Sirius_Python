import os
import boto3
import json
import constants as constants

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
dynamodb = boto3.resource('dynamodb', region_name='us-east-2')
table_name = os.environ['URLTable']
table = dynamodb.Table(table_name)

#getting the table data
urls = []

def lambda_handler(event, context):
   
        # https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
        Method = event["httpMethod"]
        url = event["body"]
        
        """ Performing CRUD Operations on DynamoDB table """
        # https://dynobase.dev/dynamodb-python-with-boto3/
        if Method == "GET":
            response = table.scan()
            data = response["Items"]
            for url in data:
                urls.append(url['url'])
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': urls
            }
        
        if Method == "POST":
            response = table.put_item(
                Item={
                    "URL": url
    
                    }
                )
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': "URL Added Successfully"
            }
        
        if Method=="PATCH":
            response=table.update_item(
                            Key={
                                "url":url
                            },
                            UpdateExpression='SET url = :url11',
                            ExpressionAttributeValues={
                                                    ':url1': url
                                                    }
                            )
            return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json'
            },
            'body': 'URL Updated Successfully'
        }
        
        if Method == "DELETE":
            response = table.delete_item(
                Key={
                    "URL": url
                }
            )
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json'
                },
                'body': "URL Deleted Successfully"
            }
        
        
    
        else:     
            return {
                    'statusCode': 200,
                    'headers': {
                        'Content-Type': 'application/json'
                    },
                    'body': "No Data Found"
                }