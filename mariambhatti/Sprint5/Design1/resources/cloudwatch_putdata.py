
import boto3

class AWSCloudWatch:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_data
    def cloudWatch_metrics(self, namespace, metric_name, dimension, value):
        # Cloud Watch Template to put metric data
        response = self.client.put_metric_data(
                Namespace=namespace,
                MetricData=[
                    {
                        'MetricName': metric_name,
                        'Dimensions': dimension,
                        'Value': value,
                        
                    },
                ]
            )
    
    # Create and enable actions on an alarm in cloudwatchs
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch.html#CloudWatch.Client.put_metric_alarm
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-using-alarms.html?highlight=cloudwatch%20alarm
    def cloudWatch_alarms(self ,AlarmName,AlarmActions,MetricName,namespace,dimensions,threshold,compop):
        response= self.client.put_metric_alarm(
            AlarmName = AlarmName,
            AlarmActions=AlarmActions,
            MetricName=MetricName,
            Namespace = namespace,
            Dimensions=dimensions,
            Threshold=threshold,
            ComparisonOperator=compop,
            Statistic = "Average",
            Period = 60,
            EvaluationPeriods = 1
        )