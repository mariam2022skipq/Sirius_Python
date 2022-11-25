import boto3
import os

class Dynamo1:
    def __init__(self):
        self.dynamoDb = boto3.resource("dynamodb", region_name="us-east-2")
        self.table_name = os.environ["Alarmtable"]
        self.table = self.dynamoDb.Table(self.table_name)

    def db_put_data(self, message_id, timestamp):
        response = self.table.put_item(
            Item={"id": message_id, "TimeStamp": timestamp})
