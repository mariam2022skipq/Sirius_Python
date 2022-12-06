import boto3
import constants as constants

class AWSCloudWatch:
    
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    
    # https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
    def cloudwatch_metric_data(self, namespace, metric_name, dimensions, value):
        
        """CloudWatch Data Template"""
        response = self.client.put_metric_data(
            Namespace= namespace,
            MetricData=[
                {
                    'MetricName': metric_name,
                    'Dimensions': dimensions,
                    'Value': value,
                },
            ]
        )
    """ Create and enable Alarm actions on an API URL alarms"""
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-using-alarms.html?highlight=cloudwatch    
    def cloudWatch_metric_alarm(self ,AlarmName,AlarmActions,MetricName,namespace,dimensions,thres,comp):
        response= self.client.put_metric_alarm(
            AlarmName = AlarmName,
            AlarmActions=AlarmActions,
            MetricName=MetricName,
            Namespace = namespace,
            Dimensions=dimensions,
            Threshold=thres,
            ComparisonOperator=comp,
            Statistic = 'Average',
            Period = 60,
            EvaluationPeriods = 1
        )