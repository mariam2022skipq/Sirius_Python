from aws_cdk import (
    aws_lambda as lambda_,
    aws_events as events_,
    aws_events_targets as target_,
    Duration,
    Stack,
    RemovalPolicy,
    aws_cloudwatch as cw_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_cloudwatch_actions as cw_actions,
    aws_dynamodb as db_,
    aws_codedeploy as cd_,
    aws_apigateway as ag_,
    CfnOutput as co_,
)
from constructs import Construct
from resources import constants as constants
from resources import constants as constants
from aws_cdk import aws_codedeploy as codedeploy_
class Sprint4Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        """ Creating the 3 lambdas in our project"""

        #Create an API Lambda which can get events from API Gateway
        lambda_role = self.create_lambda_role()
        apiLambda = self.create_lambda("ApiLambda",'./resources','API_handler.lambda_handler',lambda_role)
        wh_lambda = self.create_lambda("WHLambda",'./resources','webhealth.lambda_handler',lambda_role)
        dbLambda = self.create_lambda("DBLambda",'./resources','Db_handler.lambda_handler',lambda_role)
    


        """ Removal Policies of our resources"""
        apiLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        wh_lambda.apply_removal_policy(RemovalPolicy.DESTROY)
        dbLambda.apply_removal_policy(RemovalPolicy.DESTROY)


        """ Create API gateway and add methods and resource to it"""
        api = ag_.LambdaRestApi(self, "Mariam_Sprint4_gateway",
                                handler= apiLambda,
                                proxy=False
                                ) 

        Websites = api.root.add_resource ("Websites")                       
        items = api.root.add_resource("CRUD")
        Websites.add_method("POST")
        Websites.add_method("GET")
        Websites.add_method("PATCH")
        Websites.add_method("DELETE")
        deployment = ag_.Deployment(self, "Mariamdeployment2", api=api)
        
        
        
        #co_(self,"urlOut",value=api.url,export_name="endpoint")
        #url="https://9v8f27lr71.execute-api.us-east-2.amazonaws.com/prod/"

        #apiLambda.add_environment("Url",url)   

        """ Create a Cron job for Webhealth Lambda"""
        schedule=events_.Schedule.rate(Duration.minutes(60))
        target = target_.LambdaFunction(handler=wh_lambda)
        
        # defining a rule to convert my lambda into a cronjob by binding event and target
        rule = events_.Rule(self, "WHAppRule",
            description = "Generating events in our lambda function",
            schedule = schedule,
            targets = [target] 
            )
        rule.apply_removal_policy(RemovalPolicy.DESTROY)


        """ Create URL table for writing CRUD operations"""
        urlTable = self.create_url_table()
        urlTable.grant_full_access(apiLambda)
        apiLambda.add_environment('URLTable',urlTable.table_name)
        wh_lambda.add_environment('URLTable',urlTable.table_name)

        """Creating SNS Topic and adding subscriptions to it"""
        topic = sns_.Topic(self, "WHNotifications")
        topic.add_subscription(subscriptions_.EmailSubscription('mariambhattiskipq@gmail.com'))
        wh_lambda.add_environment('topicname',topic.topic_name)
        topic.add_subscription(subscriptions_.LambdaSubscription(dbLambda))

        """Creating a Dynamo db table for Db_Lambda"""
        dbTable = self.create_dynamoDB_table()
        dbTable.grant_full_access(dbLambda)
        dbLambda.add_environment('Table_Name',dbTable.table_name)   


        dimension={'FunctionName':wh_lambda.function_name}
        duration_metric=cw_.Metric(
                metric_name="Duration",
                namespace="AWS/Lambda",
                dimensions_map=dimension)

        invocation_metric=cw_.Metric(
                metric_name="Invocations",
                namespace="AWS/Lambda",
                dimensions_map=dimension)

        #create alarms on the metrics created above
        duration_alarm=cw_.Alarm(self, "LessDurationError",
                metric=duration_metric,
                evaluation_periods=60,     
                threshold=20000 ,
                comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD)
        
        invocation_alarm=cw_.Alarm(self, "MoreInvocationsError",
                metric=invocation_metric,
                evaluation_periods=60,     
                threshold=2,)

        version = wh_lambda.current_version
        alias = lambda_.Alias(self, "LambdaAlias",
            alias_name="Prod",
            version=version)

        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "Deploy_Alarm_Action",    
                    alias=alias,   
                    alarms=[duration_alarm,invocation_alarm],
                    deployment_config=codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE)




    def create_url_table(self):
            table = db_.Table(self, "URLTable",
            partition_key = db_.Attribute(name="URL", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,)
            return table
    def create_dynamoDB_table(self):
        table = db_.Table(self, "AlarmTable",
            partition_key = db_.Attribute(name="id", type=db_.AttributeType.STRING),
            removal_policy = RemovalPolicy.DESTROY,
            sort_key = db_.Attribute(name="Timestamp",type=db_.AttributeType.STRING),
    )
        return table

    def create_lambda(self,id,asset, handler, role):
            return lambda_.Function(self,
            id = id,
            handler = handler,
            code=lambda_.Code.from_asset(asset),
            runtime=lambda_.Runtime.PYTHON_3_9,
            role = role,
            timeout=Duration.minutes(5)
        )

    def create_lambda_role(self):
        lambda_role=iam_.Role(self, "lambda_role",
        assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))       
        return lambda_role

    








        

    