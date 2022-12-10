
# Sirius Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.

## Task 2
### Design & Develop - Consider that you are getting events in the format [{“event1”:{“attr1”: value }}] from different APIs.
#### 1) How will you parse the event to get the value?
#### 2) How will you return 10 latest events when required?
## Primary Purpose
### The Primary Purpose behind this app is to:
#### (Upon Post Request) Send a get request to 2 or more API(s) and store the data into the database while also displaying it as a response to the user.
#### (Upon Get Request) Get most recent 10 values from the database 


## Tech Stack

**Services** AWS DynamoDB, AWS Lambda, API Gateway


# CLI Code
## Installation

Install my-project with npm


### Task: Deploy the Sprint5Design2 Stack File

### Install Virtual Environment
```bash
  python -m pip install --upgrade virtualenv
```
### Enable Virtual Environment
```bash
  source .venv/bin/activate
```

### Install Prerequisites
#### pip install requirements.txt, includes prereqs like aws cdk
```bash
  python -m pip install -r requirements.txt 
```
### Export Path
```bash
  export PATH=$PATH:$(npm get prefix)/bin
```
### Synthesize code into CloudFormation
##### Presuming that we are in the sprint subfolder and in a virtual environent, we call the cdk synth to synthesize a json file in relation to my code

```bash
  cdk synth
```
### Deploy CloudFormation
##### Once the json file is synthesized, it is essential to chech the reigeon in the file. Once the confirmation of the appropiate results is achieved:
```bash
  cdk deploy
```

## Design solutions

### Design & Develop: Consider that you are getting events in the format [{“event1”:{“attr1”: value }}] from different APIs.
  
### 1) How will you parse the event to get the value?  

### 2) How will you return 10 latest events when required?


### Answer:

#### 1) How will you parse the event to get the value?  

Given that we are getting values in the format of [“event1”:{“attr1”:value}}] we have to parse it into the variable so that the value of attr1 can be attained. This is simple, we can save the json file into a variable and treat it as a list of dictionaries. It will look something like this:

    [ # List
    { # Dictionary
        'event1': #Dictionary Key
        { # Sub-Dictionary or Value of dictionary as a value
            'attr1': 0.548951 # Required Value}}]

	To get the value into a variable, we can simply write an expression resembling access to a 3 dimensional array. I.e. dict_mariam[0]['event1']['attr1']. In this case, it will return the value of attr1 which in our case was 0.548951.
  
The Parsed Event after being parsed will be sent to Dynamo DB along with Timestamp as the Partition key of dynamoDB table via LAMBDA handler through POST method of API Gateway


### 2) How will you return 10 latest events when required?

For this I will scan the table , get the table items from dynamoDb, and pass the values with Timestamp and Event_values to array and sort the array in reverse order to pass as the return status of GET method.

## Design Image




## Results


##Useful Links:

#### RemovalPolicy
https://docs.aws.amazon.com/cdk/api/v1/docs/@aws-cdk_core.RemovalPolicy.html


#### Table Properties DynamoDB
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/TableProps.html
#### Table DynamoDB
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/Table.html 
#### Declaring Environment Variable for Table Name
https://stackoverflow.com/questions/40937512/how-to-access-an-aws-lambda-environment-variable-from-python

#### Defining Scheduling datapoints_to_alarm
https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html
##### cron() indicates a time period of 1 minute between initiations
    
#### Events Target to Use an AWS Lambda function as an event rule target
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events_targets.html
        
#### Defines an EventBridge Rule in this stack. WRT aws_cdk.aws_events
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_events/Rule.html
        
#### Passing value to 'sns_topic' function so a topic can be created 
##### {Topic Rule Not Required as indicated by Documentation}
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns/Topic.html
        
#### Generating a topic for Alarm SNS, Uses an SNS topic as an alarm action.
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html

        
        
#### Use an SNS topic (my_topic) as an alarm action for Availability Alarm defined above
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html
            
#### Use an SNS topic (my_topic) as an alarm action for Latency Alarm defined above
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_cloudwatch_actions/SnsAction.html

#### SNS Subscription for Email
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_sns_subscriptions/EmailSubscription.html
        
#### Defining Lambda
https://docs.aws.amazon.com/lambda/index.html
    
#### For Sort-Key Query Limitations: 
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Query.html#:~:text=and%20Indexes%3A%20.NET-,Key%20Condition%20Expressions%20for%20Query,-To%20specify%20the
##### tl;dr: In general, DynamoDB is not designed to sort the entire table. DynamoDB uses the partition key value as input to an internal hash function. The output from the hash function determines the partition (physical storage internal to DynamoDB) in which the item will be stored. All items with the same partition key value are stored together, in sorted order by sort key value. *Therefore Sorting is not a good idea*

#### DynamoDB
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb.html

#### ShellStep
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/ShellStep.html

#### Pipelines
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines.html

#### Add Stage Options
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.pipelines/AddStageOpts.html

#### Assertions Template
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.assertions/Template.html

#### CodeDeploy
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy.html

#### Lambda Deployment Group
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html

#### Table Class
https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_dynamodb/TableClass.html
## Authors


## Author

- mariambhatti8989@gmail.com

