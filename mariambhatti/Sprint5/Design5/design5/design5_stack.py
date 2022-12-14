from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam_,
    aws_events as events_,
    aws_events_targets as target_,
    aws_cloudwatch as cw_,
    aws_sns as sns_,
    aws_s3 as s3_,
    aws_s3_deployment as s3Deploy_,
    aws_sns_subscriptions as subscriptions_,
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

class Design5Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)



        #create an API Lambda and apply removal policy to it
        lambda_role=self.lambda_role()
        bucket_lambda= self.create_lambda("bucket_Lambda" , './resources' , "bucket_handler.lambda_handler",lambda_role)
        bucket_lambda.apply_removal_policy(RemovalPolicy.DESTROY)

        # Instantiate a S3Buckect Object
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_s3/Bucket.html

        s3_bucket = self.createS3Bucket()
        s3_bucket.add_event_notification(s3_.EventType.OBJECT_CREATED, s3n.LambdaDestination(bucket_lambda))
        s3_bucket.grant_read_write(bucket_lambda)
        #bucket_lambda.add_environment("MariamBhatti_S3_Bucket",s3_bucket.bucket_name)
       

        bucket_table=self.create_bucket_table()
        bucket_table.grant_read_write_data(bucket_lambda)
        bucket_lambda.add_environment("bucket_table", bucket_table.table_name)

    def createS3Bucket(self):
        s3Bucket = s3_.Bucket(
            self, "Mariam_Bucket",
            #id=s3_id,
            removal_policy=RemovalPolicy.DESTROY,
            versioned=True,
            public_read_access=True,
            auto_delete_objects=False
        )

        return s3Bucket

    def create_bucket_table(self):
            table = db_.Table(self, "bucket_table",
            partition_key=db_.Attribute(name="Filename", type=db_.AttributeType.STRING),
            removal_policy= RemovalPolicy.DESTROY,
        )
            return table

    
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
        
    def create_lambda(self,id,asset,handler,role):
        return lambda_.Function(self,
        id=id,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9,
        role=role)


       