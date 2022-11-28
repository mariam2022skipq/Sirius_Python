#Directory for unit tests
import urllib3
import boto3
import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
import datetime
from aws_cdk import(aws_dynamodb as db_,)
from sprint3.sprint3_stack import Sprint3Stack

# code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
#test 1) Checking the creation of lambda
def test_lambda():
    #instantiating my application
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::Lambda::Function", 2)
#test2) Checking the creation of SNS topic
def test_SNS():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::SNS::Topic", 1)

#test3)checking the IAM policy for lambda 
def test_IAMPolicy():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::IAM::Policy", 1)

#test4) checking the cloudwatch alarm metrics
def test_CloudWatchMetrics():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::CloudWatch::Alarm", {
        "MetricName": "URL_AVAILABILITY",
        "MetricName": "URL_LATENCY"
    })
#test5) checking the SNS subscription
def test_SNS_Subscription():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.has_resource_properties("AWS::SNS::Subscription", {
        "Endpoint": "mariambhattiskipq@gmail.com"
    })

#test6) Check if dynamo DB table is created or not 
def test_Dynamo_Db_existence():
    app = core.App()
    stack = Sprint3Stack(app, "sprint3")
    template = assertions.Template.from_stack(stack)
    template.resource_count_is("AWS::DynamoDB::Table", 1)

#FUNCTIONAL TESTS

#1) Test if the availability function returns only 1 or zero
def getAvail():
    http=urllib3.PoolManager()
    response=http.request("GET","skipq.org")
    if response.status==200:
        return 1.0
    else:
        return 0.0

def test_avail():
    assert getAvail()==1 or getAvail()==0

#2) check if latency is less than 1
def getLatency():
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET","skipq.org")
    end=datetime.datetime.now()
    delta=end-start
    latencySec=round(delta.microseconds* .000001,6)
    return latencySec

def test_latency():
    assert getLatency() <1

#3) Check if dynamo Db is creating table correctly
def create_dynamoDB_table():
        table = db_.Table("AlarmTable",
        partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING),
        sort_key=db_.Attribute(name="Timestamp",type=db_.AttributeType.STRING))
        return table

#3) Check if dynamo Db is creating table correctly
def test_dynamo_table():
    app=core.App()
    stack=Sprint3Stack(app, "MariamBhattiStack")
    table=stack.create_dynamoDB_table
    assert table is not None

#4) Check if lambda function is created successfully 
def test_if_lambda_is_created():
    app=core.App()
    stack=Sprint3Stack(app, "MariamBhattiStack")
    lambda_exists=stack.create_lambda
    assert lambda_exists is not None