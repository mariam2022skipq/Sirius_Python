#Importing Necessary Prerequisites
from ipaddress import get_mixed_type_key
from urllib import response
import aws_cdk as cdk

from aws_cdk import (
    Duration,
    Stack, #For Stack
    aws_lambda as lambda_,
    aws_events as events_, 
    aws_events_targets as target_, 
    RemovalPolicy, 
    aws_cloudwatch as cloudwatch_, 
    aws_dynamodb as db_,
    aws_codedeploy as codeDeploy_,
    aws_apigateway as api_,
    aws_iam as iam_,
    aws_cloudwatch_actions as ca_,
    aws_apigateway as apigateway_,

)

import os
import aws_cdk.aws_cloudwatch_actions as ca_
import aws_cdk.aws_sns as sns
import aws_cdk.aws_sns_subscriptions as sns_sub 
from constructs import Construct 
import aws_cdk.aws_iam as iam 
import boto3

class Design2Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        #creating a lambda 
        lambda_role=self.lambda_role()
        apilambda= self.create_lambda("API_Lambda" , './resources' , "Api_handler.lambda_handler",lambda_role)
        apilambda.apply_removal_policy(RemovalPolicy.DESTROY)

        event_table=self.create_api_table()
        event_table.grant_read_write_data(apilambda)
        apilambda.add_environment("EventTable", event_table.table_name)

        api = apigateway_.LambdaRestApi(self, "Mariam_Design2_API1",
                                handler=apilambda,    
                                proxy=False
                            )
        api2 = apigateway_.LambdaRestApi(self, "Mariam_Design2_API2",
                                handler=apilambda,    
                                proxy=False
                            )
        api_item=api.root.add_resource("API_1_Events")
        api_item.add_method("POST")
        api_item.add_method("GET")

        api_item2=api2.root.add_resource("API_2_Events")
        api_item2.add_method("POST")
        api_item2.add_method("GET")
       


    def create_api_table(self):
        table = db_.Table(self, "EventTable",
            partition_key=db_.Attribute(name="Timestamp", type=db_.AttributeType.STRING),
            removal_policy= RemovalPolicy.DESTROY,
        )
        return table
        

 
    def create_lambda(self,id,asset,handler,role):
            return lambda_.Function(self,
                    id=id,
                    handler=handler,
                    code=lambda_.Code.from_asset(asset),
                    runtime=lambda_.Runtime.PYTHON_3_9,
                    role=role)
        

    def lambda_role(self):
            lambda_role=iam_.Role(self, "lambda_role",
            assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'))
            lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
            lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
            lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"))
            lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))
            return lambda_role