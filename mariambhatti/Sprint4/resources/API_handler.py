from unittest import result
from urllib import response
import boto3
import json
import logging
import os
from custom_encoder import customEncoder
logger = logging.getLogger()
logger.setLevel(logging.INFO)

#Access table through lambda function
tablename = os.getenv("CRUD_URL_Table")
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(tablename)

#define methods
getMethod = "GET"
postMethod = "POST"
patchMethod = "PATCH"
deleteMethod = "DELETE"

#defining path for the event
websitepath = "/Websites"

def lambda_handler(event, context):
    logger.info(event)
    httpMethod = event["httpMethod"]
    path = event["path"]

    if httpMethod == getMethod and path == websitepath:
        response = getWebsite(event['queryStringParameters']['websiteId'])
    elif httpMethod == postMethod and path == websitepath:
        response = addWebsite (json.loads(event['body']))
    elif httpMethod == patchMethod and path == websitepath:
        requestBody = json.loads(event['body'])
        response = updateWebsite (requestBody['websiteId'], requestBody['updateKey'], requestBody['updateValue'])
    elif httpMethod == deleteMethod and path == websitepath:
        requestBody = json.loads(event['body'])
        response = removeWebsite (requestBody['websiteId'])
    else:
        response = buildResponse(404, 'not found')
    
    return response

#defining the Getwebsite method after parsing the APIGateway JSON File
def getWebsite(websiteId):
    try:
        response = table.get_item (
            Key = {
                'websiteId': websiteId
            }
        )
        if 'Item' in response:
            return buildResponse(200, response['Item'])
        else:
            return buildResponse (404, {'Message': 'websiteId: %s not found' % websiteId})
    except:
        logger.exception ('Do you custom error handling here')

#defining the addWebsite API Gateway HTTP method for adding the URL to the table
def addWebsite(requestBody):
    try:
        table.put_item (Item = requestBody)
        body = {
            'Operation': 'SAVE',
            'Message': 'SUCCESS',
            'Item': requestBody
        }
        return buildResponse(200, body)
    except:
        logger.exception ('Do you custom error handling here')

def updateWebsite(websiteId, updateKey, updateValue):
    try:
        response = table.update_item(
            Key = {
                'websiteId': websiteId
            },
            UpdateExpression = 'set %s = :value' % updateKey,
            ExpressionAttributeValues = {
                ':value' : updateValue
            },
            ReturnValues = 'UPDATED_NEW' 
        )
        body = {
            'Operation': 'UPDATE',
            'Message': 'SUCCESS',
            'UpdatedAttrebutes': response
        }
        return buildResponse (200,body)
    except:
        logger.exception ('Do you custom error handling here')

def removeWebsite(websiteId):
    try:
        response = table.delete_item(
            Key = {
                'websiteId': websiteId
            },
            ReturnValues = 'ALL_OLD'
        )
        body = {
            'Operation': 'DELETE',
            'Message': 'SUCCESS',
            'deletedItem': response
        }
        return buildResponse(200,body)
    except:
        logger.exception ('Do you custom error handling here')

def buildResponse(statusCode, body = None):
    response = {
        'statusCode': statusCode,
        'headers': {
            'Content-Type':'application/json',
            'Access-Control-Allow-Origin' : '*'
        }
    }
    if body is not None:
        response['body'] = json.dumps(body, cls= customEncoder)
    return response



    