import boto3
import datetime

class AWSCloudWatch:
    def __init__(self):
        #creating a boto3 client for putting Cloudwatch Metric data
        self.client=boto3.client('cloudwatch')
    def cloudwatch_metric_data(self, namespace, metric_name, dimensions, value):
        # https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
        response =self.client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Value': value,
                },
            ]
        )

        

