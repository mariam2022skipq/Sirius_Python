import boto3
import constants as constants

class cloudwatchPutAlarm:
    def __init__(self):
        self.client = boto3.client('cloudwatch')
    
    #function that creates alarms to be monitored on cloudwatch
    def putAlarm(self,AlarmName,AlarmActions,metric_name,namespace,dimensions,comparisonOperator,threshold):
        
        response = self.client.put_metric_alarm(
            AlarmName = AlarmName,
            AlarmActions = AlarmActions,
            MetricName = metric_name,
            Namespace = namespace,
            Dimensions = dimensions,
            ComparisonOperator = comparisonOperator,
            Threshold = threshold,
            EvaluationPeriods =1, 
            Period = 180,
            Statistic='Average'
                                    
        )
