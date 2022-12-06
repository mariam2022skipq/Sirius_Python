from aws_cdk import (
    Duration,
    Stack,
    # aws_sqs as sqs,
    aws_iam as iam_,
    aws_events as events_,
    aws_events_targets as target_,
    aws_cloudwatch as cw_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    RemovalPolicy,
    aws_apigateway as agw,
    aws_lambda as lambda_,
    aws_dynamodb as db_,
    aws_events as events_,
    aws_events_targets as target_, 
    aws_apigateway as apigateway_,
)
from constructs import Construct
class Design1Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #create an API Lambda and apply removal policy to it
        lambda_role=self.lambda_role()
        apilambda= self.create_lambda("API_Lambda" , './resources' , "Api_handler.lambda_handler",lambda_role)
        apilambda.apply_removal_policy(RemovalPolicy.DESTROY)

        #creating lambda for dynamo DB in which CRUD values will be stored
        dbLambda = self.create_lambda("DB_fetching_Lambda", './resources', 'db_fetching_lambda.lambda_handler',lambda_role)
        dbLambda.apply_removal_policy(RemovalPolicy.DESTROY)

        #converting our db_lambda to a cron job
        schedule=events_.Schedule.rate(Duration.minutes(30))

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events_targets/LambdaFunction.html
        target=target_.LambdaFunction(handler=dbLambda)

        # https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/README.html
        rule = events_.Rule(self, "argumentRule",
            schedule=schedule,
            targets=[target])

        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        #adding a topic for SNS email notification and add subscription to it
        topic = sns_.Topic(self, id = "Email_Notification")
        topic.add_subscription(subscriptions_.EmailSubscription("mariambhattiskipq@gmail.com"))
        dbLambda.add_environment("Email_Notification",topic.topic_name)
        topic.add_subscription(subscriptions_.LambdaSubscription(dbLambda)) 

        #configuring our restful API and POST method
        api = apigateway_.LambdaRestApi(self, "Mariam_Design1_API",
                                handler=apilambda,    
                                proxy=False
                            )
        api_item=api.root.add_resource("Argument_CRUD")
        api_item.add_method("POST")
        api_item.add_method("GET")
        api_item.add_method("PATCH")
        api_item.add_method("DELETE")


        #creating a dynamoDB table for writing API CRUD values
        apiTable=self.create_api_table()
        apiTable.grant_read_write_data(apilambda)
        apilambda.add_environment("ArgTable", apiTable.table_name)
        dbLambda.add_environment("ArgTable", apiTable.table_name)
        dbLambda.add_environment("snsTopic", topic.topic_name)

    def create_api_table(self):
        table = db_.Table(self, "ArgTable",
            partition_key=db_.Attribute(name="ARG", type=db_.AttributeType.STRING),
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
        return lambda_role
        
    def create_lambda(self,id,asset,handler,role):
        return lambda_.Function(self,
        id=id,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9,
        role=role)
