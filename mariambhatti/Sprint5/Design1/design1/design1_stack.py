from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    RemovalPolicy,
    aws_apigateway as agw,
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as target_, 
)
from constructs import Construct
class Design1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #create an API Lambda and apply removal policy to it
        lambda_role=self.create_lambda_role()
        api_lambda= self.create_lambda("API_Lambda" , './resources' , "Api_handler.lambda_handler",lambda_role)
        api_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        #adding a topic for SNS email notification and add subscription to it
        topic = sns_.Topic(self, id = "Email_Notification")
        topic.add_subscription(subscriptions_.EmailSubscription("mariambhattiskipq@gmail.com"))
        api_lambda.add_environment("Email_Notification",topic.topic_name)

        #configuring our restful API and POST method
        api = agw.RestApi(self,"UmarApi")
        api=api.root.add_resource("UmarApi") 
        api.add_method ("POST" , agw.LambdaIntegration(api_lambda))
    
    def create_lambda_role(self):
        lambda_role=iam_.Role(self, "lambda_role",
        assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))
        return lambda_role
        
    def create_lambda(self,id,asset,handler,role):
        return lambda_.Function(self,
        id=id,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9,
        role=role)
