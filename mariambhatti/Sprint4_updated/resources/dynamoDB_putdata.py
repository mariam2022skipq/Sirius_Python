import boto3
import os

class DynamoDB:
    def __init__(self) -> None:
        """ Get DynamoDb Table from Environment Variables and setting the table name from environment variable """
        # https://docs.aws.amazon.com/lambda/latest/dg/configuration-envvars.html#configuration-envvars-retrieve
        self.table_name = os.environ.get('Table_Name')
        
        self.dynamoDb = boto3.resource("dynamodb", region_name="us-east-2")
        self.table = self.dynamoDb.Table(self.table_name)

    def put_Data(self, message_id, timestamp):
        """ Put Event Data in DynamoDB Table"""
        # https://dynobase.dev/dynamodb-python-with-boto3/#list-tables
        response = self.table.put_item(
        Item={
            "id": message_id,
            "Timestamp": timestamp,
        }
    )