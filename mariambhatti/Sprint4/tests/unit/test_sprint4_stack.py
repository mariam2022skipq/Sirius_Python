#Directory for unit tests
import urllib3
import boto3
import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
import datetime
from aws_cdk import(aws_dynamodb as db_,)
from sprint4.sprint4_stack import Sprint4Stack

# code ref: https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html
#test 1) Checking the creation of lambda
#def test_lambda():
    #instantiating my application
   # app = core.App()
    #stack = Sprint4Stack(app, "sprint4")
    #template = assertions.Template.from_stack(stack)
    #template.resource_count_is("AWS::Lambda::Function", 4)
#test2) Checking the creation of SNS topic

#test6) Check if dynamo DB table is created or not 
#def test_Dynamo_Db_existence():
    #app = core.App()
    #stack = Sprint4Stack(app, "sprint4")
    #template = assertions.Template.from_stack(stack)
    #template.resource_count_is("AWS::DynamoDB::Table", 2)

#FUNCTIONAL TESTS

#1) Test if the availability function returns only 1 or zero
def getAvailability():
    http=urllib3.PoolManager()
    response=http.request("GET","skipq.org")
    if response.status==200:
        return 1.0
    else:
        return 0.0

def test_availability():
    assert getAvailability()==1 or getAvailability()==0

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

