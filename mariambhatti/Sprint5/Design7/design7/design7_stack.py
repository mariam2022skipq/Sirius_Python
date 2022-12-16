from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam_,
    aws_events as events_,
    aws_events_targets as target_,
    aws_s3 as s3_,
    aws_s3_deployment as s3Deploy_,
    RemovalPolicy,
    aws_apigateway as agw,
    aws_lambda as lambda_,
    aws_dynamodb as db_,
    aws_events as events_,
    aws_events_targets as target_, 
    aws_apigateway as apigateway_,
    aws_s3_notifications as s3n,
)
from constructs import Construct
from ipaddress import get_mixed_type_key
from urllib import response
import aws_cdk as cdk

class Design7Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)


        lambda_role=self.lambda_role()
        signed_lambda= self.create_lambda("signed_Lambda" , './resources' , "signed_handler.lambda_handler",lambda_role)
        signed_lambda.apply_removal_policy(RemovalPolicy.DESTROY)


        s3_bucket = self.createS3Bucket()
        #s3_bucket.add_event_notification(s3_.EventType.OBJECT_CREATED, s3n.LambdaDestination(signed_lambda))
        s3_bucket.grant_read_write(signed_lambda)

        api = apigateway_.LambdaRestApi(self, "Mariam_Design7_API",
                                handler=signed_lambda,    
                                proxy=False
                            )

        #Adding root and resources to API gateway
        api_item=api.root.add_resource("API_Signed")
        api_item.add_method("POST")
        #api_item.add_method("GET")


    def createS3Bucket(self):
        s3_Bucket = s3_.Bucket(
            self, "Mariam_Signed_Bucket",
            #id=s3_id,
            removal_policy=RemovalPolicy.DESTROY,
            versioned=True,
            public_read_access=False,
            auto_delete_objects=False
        )

        return s3_Bucket

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
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonSESFullAccess"))
        return lambda_role

    


    
    
        