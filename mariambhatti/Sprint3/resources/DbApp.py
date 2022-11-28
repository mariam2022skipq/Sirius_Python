import boto3
import os
from Db_putdata import Dynamo1


def lambda_handler(event, context):
    #creating a dynamo object of db_putdata
    dynamo_obj = Dynamo1()
    #extracting message ID and timestamp from JSOn file
    message_id = event["Records"][0]["Sns"]["MessageId"]
    timestamp = event["Records"][0]["Sns"]["Timestamp"]

    #passing the data to be put into message id and time stamp in dynamoDB
    dynamo_obj.db_put_data(message_id, timestamp)
    








