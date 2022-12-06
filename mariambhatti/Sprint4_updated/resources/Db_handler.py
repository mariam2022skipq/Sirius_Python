from dynamoDB_putdata import DynamoDB

def lambda_handler(event, context):
    """ Extract Event Data for Table for SNS notifications """

    message_id = event["Records"][0]["Sns"]["MessageId"]
    timestamp = event["Records"][0]["Sns"]["Timestamp"]
    
    """ Creating object for inserting values in DynamoDb"""
    dynamoDb_obj = DynamoDB()
    dynamoDb_obj.put_Data(message_id,timestamp)