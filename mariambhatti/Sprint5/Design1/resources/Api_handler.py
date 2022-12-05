import boto3
import os
from cloudwatch_putdata import CloudWatch

topicname=os.environ["Email_Notification"]
AlarmActions = ["arn:aws:sns:us-east-2:315997497220:{topicname}".format(topicname=topicname)]
Metric_Name = "mariam_argument_metric"
Alarm_Name = "mariam_argument_alarm"
namespace= "MariambhattiSprint6"

def lambda_handler(event,context):
    #this API lambda_handler function accepts argument as a API call which is parsed as int an threshold is checked
    arg=event["body"]
    dimensions = [{"Name" : "ARGUMENT" , "Value" : arg}]
    #print(arg)
    cloudwatch_object = CloudWatch()
    cloudwatch_object.cloudWatch_metric_data(namespace,Metric_Name,dimensions,int(arg))
    cloudwatch_object.cloudWatch_metric_alarm(Alarm_Name,AlarmActions,Metric_Name,namespace,dimensions,10,"GreaterThanThreshold")