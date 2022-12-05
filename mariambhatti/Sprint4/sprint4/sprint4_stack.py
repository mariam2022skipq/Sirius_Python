import aws_cdk as cdk
from aws_cdk import(
    aws_lambda as lambda_ ,
    Stack,
    RemovalPolicy,
    Duration,
    aws_events as events_,
    aws_events_targets as target_,
    aws_cloudwatch as cw_,
    aws_iam as iam_,
    aws_sns as sns_,
    aws_sns_subscriptions as subscriptions_,
    aws_sns_subscriptions as sub_,
    aws_cloudwatch_actions as cw_actions_,
    aws_apigateway as apigateway,
    aws_lambda_event_sources as es,
    aws_dynamodb as db_,)

from resources import constants as constants
from aws_cdk import aws_codedeploy as codedeploy_
from aws_cdk.aws_lambda_event_sources import SnsEventSource
namespace="MariamBhattisprint2Namespace"
AvailabilityMetric="URL_AVAILABILITY"
LatencyMetric="URL_LATENCY"
#bring metric in infrastructure to create alarm
 # aws_sqs as sqs,
from constructs import Construct


class Sprint4Stack(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        lambda_role=self.create_lambda_role()
        #creating  a dynamoDB lambda and Db_lambda for inserting SNS event data to dynamoDB
        fn = self.create_lambda("WHlambda", './resources', 'Webhealthapp.lambda_handler',lambda_role)
        dbLambda= self.create_lambda("DBlambda", './resources', 'DbApp.lambda_handler',lambda_role)
        #ApiLambda = self.create_lambda("APILambda", "./resources", "API.lambda_handler",lambda_role)
        ApiLambda = lambda_.Function(
            self,
            id="MariamLambda",
            handler="API_handler.lambda_handler",
            code=lambda_.Code.from_asset("./resources/"),
            runtime=lambda_.Runtime.PYTHON_3_8,
            role=lambda_role,
            timeout=Duration.minutes(5),
        )

        #this is a dynamoDB table which will write CRUD operations
        CRUD_dynamo_table = db_.Table(self,"CRUD_URL_Table",
            partition_key=db_.Attribute(name="Website_id", type=db_.AttributeType.STRING))
        #extracting CRUD table name for ease
        #crudTable=CRUD_dynamo_table.table_name

        ApiLambda.add_environment("CRUD_URL_Table",CRUD_dynamo_table.table_name)
        fn.add_environment("CRUD_tablewebHealth2",CRUD_dynamo_table.table_name)
        
        CRUD_dynamo_table.grant_full_access(fn)
        CRUD_dynamo_table.grant_full_access(ApiLambda)

        #removal policies for the destruction of lambda
        fn.apply_removal_policy(RemovalPolicy.DESTROY)
        dbLambda.apply_removal_policy(RemovalPolicy.DESTROY)
        ApiLambda.apply_removal_policy(RemovalPolicy.DESTROY)


        #table to write/read/update/get URLS which will come through HTTP requests

        #------------------REST API Gateway------------------
        #https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_apigateway/LambdaRestApi.html        

        # new Lambda-backed REST Api
        api = apigateway.LambdaRestApi(self, "mariamBhatti_API",
            handler=ApiLambda,
            proxy=False
        )
        #Api resources
        health = api.root.add_resource ("Health")
        WebCrawler =api.root.add_resource("WebCrawler")
        Websites = api.root.add_resource ("Websites")



        #Api Methods
        health.add_method("GET")
        Websites.add_method("POST")
        Websites.add_method("GET")
        Websites.add_method("PATCH")
        Websites.add_method("DELETE")
        WebCrawler.add_method("GET")
        

        #API Deployment
        deployment = apigateway.Deployment(self, "Mariamdeployment2", api=api)


        #defining a rule to convert my lambda into a cron job,defining target of event, and defining rule to bind event and target
        schedule=events_.Schedule.rate(Duration.minutes(10))
        target=target_.LambdaFunction(handler=fn)
        rule=events_.Rule(self, "WHAppRule",
            schedule=schedule,
            targets=[target])
        rule.apply_removal_policy(RemovalPolicy.DESTROY)

        #create an sns topic and subscriptions
        topic=sns_.Topic(self, "WHealth_Notification")
        #now we have to connect my sns and its topic
        topic.add_subscription(subscriptions_.EmailSubscription('mariambhattiskipq@gmail.com'))
        #topic.add_subscription(subscriptions_.LambdaSubscription(dbLambda))
        dbLambda.add_event_source(SnsEventSource(topic))

        topicName = topic.topic_name
        fn.add_environment("topicName", topicName)



        #Define a DynamoDB table
        dbTable=self.create_dynamoDB_table()
        #Grant access of this dynamo DB to DB_Lambda
        dbTable.grant_read_write_data(dbLambda)
        dbLambda.add_environment('AlarmTable',dbTable.table_name)



        """now we will create alarms for both the metrics availability and latency"""
        #    dimensions={'url':url}
        #    availability_metric=cw_.Metric(
        #        metric_name=constants.AvailabilityMetric,
        #        namespace=constants.namespace,
        #        dimensions_map=dimensions)

        #    availability_alarm=cw_.Alarm(self, url + "notOk",
        #        metric=availability_metric,
        #        evaluation_periods=60,     
        #        threshold=1,
        #        comparison_operator=cw_.ComparisonOperator.LESS_THAN_THRESHOLD)
         #   availability_alarm.add_alarm_action(cw_actions_.SnsAction(topic))
         #   latency_metric=cw_.Metric(
         #       metric_name=constants.LatencyMetric,
         #       namespace=constants.namespace,
         #       dimensions_map=dimensions
        #
        #    latency_alarm=cw_.Alarm(self, url + "Ok",
        #        metric=latency_metric,
        #        evaluation_periods=60,
        #        threshold=0.2,
        #        comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD)
        #    latency_alarm.add_alarm_action(cw_actions_.SnsAction(topic))
        #helooooooo
        #Now here I will create Alarms on various metrics for monitoring the health of our application:WebHealth lambda

        #Defining the metrics
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda/Function.html

        dimension={'FunctionName':fn.function_name}
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
                evaluation_periods=1,     
                threshold=0.2 ,
                comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD)
        
        invocation_alarm=cw_.Alarm(self, "MoreInvocationsError",
                metric=invocation_metric,
                evaluation_periods=1,     
                threshold=5,
                comparison_operator=cw_.ComparisonOperator.GREATER_THAN_THRESHOLD)

        # used to make sure each CDK synthesis produces a different Version
        #Now i will configure deployment groups and deployment configurations
        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy.html

        version = fn.current_version
        alias = lambda_.Alias(self, "LambdaAlias",
            alias_name="Prod",
            version=version)

        #https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codedeploy/CfnDeploymentConfig.html
        deployment_group = codedeploy_.LambdaDeploymentGroup(self, "Deploy_Alarm_Action",    
                    alias=alias,   
                    alarms=[duration_alarm,invocation_alarm],
                    deployment_config=codedeploy_.LambdaDeploymentConfig.LINEAR_10_PERCENT_EVERY_1_MINUTE)


    def create_lambda(self,id,asset,handler,role):
        return lambda_.Function(self,
        id=id,
        handler=handler,
        code=lambda_.Code.from_asset(asset),
        runtime=lambda_.Runtime.PYTHON_3_9,
        role=role)

    def create_lambda_role(self):
        lambda_role=iam_.Role(self, "lambda_role",
        assumed_by=iam_.ServicePrincipal('lambda.amazonaws.com'))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaVPCAccessExecutionRole"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("CloudWatchFullAccess"))
        lambda_role.add_managed_policy(iam_.ManagedPolicy.from_aws_managed_policy_name("AmazonDynamoDBFullAccess"))
        return lambda_role

    def create_dynamoDB_table(self):
        table = db_.Table(self, "AlarmTable",
        partition_key=db_.Attribute(name="id", type=db_.AttributeType.STRING),
        sort_key=db_.Attribute(name="Timestamp",type=db_.AttributeType.STRING))
        return table

            
