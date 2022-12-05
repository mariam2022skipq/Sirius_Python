import boto3


class CloudWatch:
    def __init__(self):
        self.client = boto3.client("cloudwatch")
        #Creating CloudWatch metrics and Cloudwatch alarms using boto3 Client
    def cloudWatch_metric_data(self, namespace, metric_name, dimensions, value):
        response = self.client.put_metric_data(
            Namespace=namespace,
            MetricData=[
                {
                    "MetricName": metric_name,
                    "Dimensions": dimensions,
                    "Value": value,
                },
            ],)

    def cloudWatch_metric_alarm (self ,AlarmName,AlarmActions,MetricName,namespace,dimensions,thres,comp):
        response= self.client.put_metric_alarm(
            AlarmName = AlarmName,
            AlarmActions=AlarmActions,
            MetricName=MetricName,
            Namespace = namespace,
            Dimensions=dimensions,
            Threshold=thres,
            ComparisonOperator=comp,
            Statistic = "Average",
            Period = 60,
            EvaluationPeriods = 1
        )
    
