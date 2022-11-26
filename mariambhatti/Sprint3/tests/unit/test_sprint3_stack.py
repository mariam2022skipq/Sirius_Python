#Directory for unit tests
import aws_cdk as core
import aws_cdk.assertions as assertions
import pytest
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