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

        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/README.html
        lambda_role=self.lambda_role()
        signed_lambda= self.create_lambda("signed_Lambda" , './resources' , "signed_handler.lambda_handler",lambda_role)
        signed_lambda.apply_removal_policy(RemovalPolicy.DESTROY)


        s3_bucket = self.createS3Bucket()
        s3_bucket.grant_read_write(signed_lambda)
        signed_lambda.add_environment(key="MariamSignedBucket", value=s3_bucket.bucket_name)

        """ Creating API Gateway """
        # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/README.html
        api = apigateway_.LambdaRestApi(self, "Mariam_Design7_API",
                                handler=signed_lambda,    
                                proxy=False
                            )

        #Adding root and resources to API gateway
        api_item=api.root.add_resource("API_Signed")
        api_item.add_method("POST")
        #api_item.add_method("GET")

    """ Creating API Gateway """
    #https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
    def createS3Bucket(self):
        s3_Bucket = s3_.Bucket(
            self, "MariamSignedBucket",
            #id=s3_id,
            removal_policy=RemovalPolicy.DESTROY,
            #versioned=True,
            public_read_access=False,
            auto_delete_objects=False
        )

        return s3_Bucket

    """ 
        Creates lambda function from the construct library.
        
        Parameters:
                assets (str) - Stack file path for the application to be deployed on lambda.
                handler (str) - Handler function to execute.
                role (str) - IAM role for lambda function.
        Return:
                Lambda fucntion
    
    """
    # https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/README.html
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
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonS3FullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonAPIGatewayInvokeFullAccess"))
        return lambda_role

    


    
    
        