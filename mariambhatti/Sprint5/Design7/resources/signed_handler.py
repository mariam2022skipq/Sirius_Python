import json
import os
import boto3
from datetime import datetime
import uuid

#concept taken from the below link
#https://sookocheff.com/post/api/uploading-large-payloads-through-api-gateway/

#Getting the bucket name from environment variables
signed_bucket = os.environ['MariamSignedBucket']
def lambda_handler(event, context):
    #Using boto3 client to generate Pre-signed URL
    s3 = boto3.client("s3")
    # https://docs.aws.amazon.com/lambda/latest/dg/services-apigateway.html
    method = event["httpMethod"]

    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url
    if method == "POST": 
        queryStringParameters = event["queryStringParameters"]
        file_name = queryStringParameters["file_name"]
        signedURL = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": signed_bucket,
                "Key": file_name,
            },
            ExpiresIn=8000,
        )

        return {"statusCode": 200,
                 "body": json.dumps(signedURL)}

   


