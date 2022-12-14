import boto3
import json
import os
import uuid
import re
from collections import Counter
#from aws_cdk import aws_s3 as s3_


def lambda_handler(event, context):
    s3Client = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key=str(event['Records'][0]['s3']['object']['key'])

    response=s3Client.get_object(Bucket=bucket,Key=key)
    #read and decode
    data=response['Body'].read().decode('utf-8')
    #process the data 
    parsed_data= re.sub(r'\W+', ' ', data)
    processed_data = parsed_data.split()
    dic_count = Counter(processed_data)

    #https://www.learnaws.org/2020/12/18/aws-ses-boto3-guide/
    #Before sending email using SES, we need to verigy it
    ses_client = boto3.client("ses", region_name="us-east-2")
    response = ses_client.verify_email_identity(
    EmailAddress="mariambhattiskiq@gmail.com" )

    ses_client = boto3.client("ses", region_name="us-west-2")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "mariambhattiskiq@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                     "Data": json.dumps(dic_count),
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": json.dumps("Word Count of "+ key),
            },
        },
        Source="abhishek@learnaws.org",
    )


    #writing batch data to the table
    dynamodb=boto3.resource('dynamodb',region_name='us-east-2')
    table_name = os.environ['bucket_table']
    table = dynamodb.Table(table_name)
    for i,j in dic_count.items():
            response = table.put_item(Item={
                "Word": i,
                "Count": str(j),
                "Filename": key
            })
   
    return {
        'statusCode': 200,
        'body': json.dumps('Success Data Sent!')
    }

    
       