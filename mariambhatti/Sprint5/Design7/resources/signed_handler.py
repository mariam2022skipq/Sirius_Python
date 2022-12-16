import json
import os
import boto3
from datetime import datetime

#Getting the bucket name from environment variables
signed_bucket = os.environ['Mariam_Signed_Bucket']
def lambda_handler(event, context):
    #Using boto3 client to generate Pre-signed URL
    s3 = boto3.client("s3")
   
    #concept taken from the below link
    #https://sookocheff.com/post/api/uploading-large-payloads-through-api-gateway/

    method = event["httpMethod"]
    queryStringParameters = event["queryStringParameters"]
    file_name = queryStringParameters["file_name"]
    #key = event["body"]["key"]

    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.generate_presigned_url
    if method == "POST":
        signedURL = s3.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": signed_bucket,
                "Key": file_name,
            },
            ExpiresIn=3600,
        )

    return {"statusCode": 200, "body": json.dumps(signedURL)}


