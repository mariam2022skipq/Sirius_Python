import boto3
import json
import os
import uuid
import re
from collections import Counter
#from aws_cdk import aws_s3 as s3_

dynamodb=boto3.resource('dynamodb',region_name='us-east-2')
table_name = os.environ['bucket_table']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    s3Client = boto3.client('s3')
    bucket = event['Records'][0]['s3']['bucket']['name']
    key=str(event['Records'][0]['s3']['object']['key'])

    response=s3Client.get_object(Bucket=bucket,Key=key)
    #read and decode
    data=response['Body'].read().decode('utf-8')
    #process the data 
    parsed_data= re.sub(r'\W+', ' ', data)
    temp = parsed_data.split()
    word_count={}
    for i in range(len(temp)):
        if str(temp[i]) in word_count:
            word_count[str(temp[i])] +=1
        else:
            word_count[str(temp[i])]=1
    
    table.put_item(Item={"Filename": str(key), "Word_count": str(word_count)})


    #https://www.learnaws.org/2020/12/18/aws-ses-boto3-guide/
    #Before sending email using SES, we need to verigy it
    ses_client = boto3.client("ses", region_name="us-east-2")
    response = ses_client.verify_email_identity(
    EmailAddress="mariambhattiskiq@gmail.com" )


    ses_client = boto3.client("ses", region_name="us-east-2")
    CHARSET = "UTF-8"

    response = ses_client.send_email(
        Destination={
            "ToAddresses": [
                "mariambhattiskipq@gmail.com",
            ],
        },
        Message={
            "Body": {
                "Text": {
                    "Charset": CHARSET,
                    "Data": f"FileName: {key}\nFreq : {word_count} ",
                }
            },
            "Subject": {
                "Charset": CHARSET,
                "Data": f"Word Count  in {key}",
            },
        },
        Source="mariambhattiskipq@gmail.com",
    )

    


    
    

    
       