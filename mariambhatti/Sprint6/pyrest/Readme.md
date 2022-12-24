SPRINT 6 Project : Dockerizing RESTFUL CRUD API Gateway Project for Web health Application!
#  RESTFUL CRUD API Gateway Project for Web health Application!
### Use docker to build API test clients using pyresttest. 

#### This is a Dockerized  AWS CRUD API Gateway application for the Web Crawler app to populate a URL DynamoDB table to perform REST API CRUD operations and monitor the resource web health.

##### [Back-to-Top](#back-to-top)
---

## **Table of Contents:**

* ### [Overview](#overview-1)
* ### [CRUD API Gateway](#crud-api-gateway-1)
* ### [CI/CD](#cicd-pipeline)
* ### [Objective](#objective-1)
* ### [AWS Services](#aws-services-1)
* ### [Non AWS Services](#non-aws-services-1)
* ### [Getting Started](#getting-started-1)

    * ### [Environment Setup](#environment-setup-1)

    * ### [Project Setup](#project-setup-1)

    * ### [Project Deployment](#project-deployment-1)

* ### [Results](#results-1)
    
    * ### [API Gateway]()

    * ### [DynamoDB](#dynamodb-screenshots)

    * ### [SNS Notifications](#sns-notifications-screenshots)

    * ### [CloudWatch Alarms](#cloudwatch-alarm-screenshots)

    * ### [CodePipeline](#codepipeline-screenshots)

    * ### [Unit Functional & Integration Tests](#unit-functional-and-integration-tests)


 * ### [References](#references-1)
 * ### [Useful Commands](#useful-commands-1)
 * ### [Author Contact](#author-contact-1)

<br />


>  ## Overview
 <br />
 
## Use docker to build API test clients using pyresttest. 
Publish the built images to Elastic Container Registry (ECR). Continuously run functional and security API tests as cron-job on local machines. These tests will exercise the web crawler’s CRUD endpoint built in Sprint 4. 
Deploy API test clients from (1) on an EC2 instance. Build and push API test dockers through CodePipeline. Push API test results into CloudWatch. Setup alarming and notification on API test metrics. Extend tests in each stage.

This project builds a CRUD API Gateway endpoint for our Web Crawler application which further populates a URL dynamo DB to perform REST API CRUD operation
Further , we can monitor the web health of all the URLS provided by the client through API gateway endpoint with CI/CD implemented with a CRUD business
logic.
The CRUD operation is performed by a fully managed AWS service: API GATEWAY. It is a restful API and follows the following Protocols of HTTP
1) GET
2) PATCH
3) UPDATE
4) DELETE
Upon method request and successful method operation an **HTTP statusCode:200** is sent in response and the data is modified in the DynamoDB table, which is further sent to the web health app to calculate the web health metrics and 
raise **Alarms** and actions in **CloudWatch** using **Python boto3 SDK**.


Availability metric is  used to check the health of the websites.Upon method request and successful method operation an **HTTP statusCode:200** is sent 
in response and the data is modified in the DynamoDB table, which is further sent to the web health app to calculate the web health metrics and raise **Alarms** and actions in **CloudWatch** using **Python boto3 SDK**. 

Latency metric his metric is the combined values of domain lookup time, connect time and response time. Latency: Putting the application, the server and the DNS response times aside for a moment, obviously the network can be a big factor when measuring performance. This metric calculates the amount of delay on a network.
 **Low latency** or **High latency** depends upon the performance of that specific website.
These metrics are defined by boto S3 client Logged by Amazon Cloudwatch and Cloudwatch raises an Alarm whenever these metrics cross a specific threshold
AWS SNS services is linked with cloudwatch which sends a detailed notification to the subscriber of the topic and sends an Email about the
threshold breach and alarm.
Also,this SNS will trigger a **Lambda Funtion** which will then save that alarm information in a **DynamoDB Table**.
 
 
<br />
<br />

>  ## CRUD API Gateway
 <br />

Amazon API Gateway is a fully managed service that makes it easy for developers to create, publish, maintain, monitor, and secure APIs at any scale. APIs act as the "front door" for applications to access data, business logic, or functionality from your backend services. Using API Gateway, you can create RESTful APIs and WebSocket APIs that enable real-time two-way communication applications. API Gateway supports containerized and serverless workloads, as well as web applications.
The RESTFUL CRUD API Gateway is implemented by using **AWS API Gateway** which uses the **HTTP** Protocol with the request and response messages to perform the RESTFUL API operations of Create, Read, Update and Delete. From the **AWS API Gateway** i have used the Lambda invoked API Gateway to integrate the API Lambda with the RESTFUL endpoint to perform the following 4 methods:
 <br /> 

 * **GET**
 * **POST**
 * **PATCH**
 * **DELETE**
<br />
The above mentioned methods do the following function

The **GET** method performs the functionality to extract all available records using the scan function on the URL DynamoDB table. In case the records are found an **HTTP statusCode:200** is sent along with the scanned data in the body of the **response**. 
<br/>

The **POST** method performs the functionality to send the data in the **request** body to the URL DynamoDB table and upon successful put function an **HTTP statusCode:200** is sent and data is written in the DynamoDB table.
<br />

The **PATCH** method performs the functionality to send a key and reference value to update the existing records value with the sent value using the update function, in response an **HTTP statusCode:200** is sent and data is overwritten in the DynamoDB table for the respective field.
<br />

The **DELETE** method  performs the functionality to delete a record in the table by using the delete function. A key:value pair is sent the request body and upon successful delete operation an **HTTP statusCode:200** is sent and the respective data is deleted in the DynamoDB table.

 Main objective of this CRUD API Gateway application is to get a clear understanding of **How to build a CRUD API Gateway endpoint for the Web Crawler app to populate a URL DynamoDB table to perform REST API CRUD operations, so that we can monitor the web health of the URL resources and implement CI/CD with CRUD business logic**.
<br />
<br />

 > ## CI/CD Pipeline
 <br />
### The CI/CD pipeline takes docker image container from the github source code . The pyrest tests for GET,POST and DELETE method and bencmark tests for these files are also present in pyrest folder along with Dockerfile.
### The Dockerfile is composed of prebuild docker image from thoom/pyresttest and contains pre-built image of Docker , working directory, entry point and commands
 The CI/CD Pipeline is implemented using **AWS CodePipeline** as the base, **Github** as a **Source**, **AWS CodeBuild** as the build service and **AWS CodeDeploy** for deployment.
 The multi-stage pipeline CI/CD is divided into 2 stages with unit, functional and integration tests being perfomed, also Manual approval is required in pre production stage:
 <br /> 

 * **Beta (Unit, Functional and Integration Tests)**
 * **Prod (Manual Approval)**
<br />

The **Beta** stage performs the 5 Unit tests and 1 functional test using **Pytest** fixtures and for resource count, resource properties and assertions match with stack templates and creation of dynamodb table in stack.

<br /> 

The **Prod** stage performs the **Manual Approval** step, which requires the user to review and approve or reject the deployment to Production.
<br />
<br />
> ## AWS-Services
 <br />

 The services used for deployment of this project are metn:

 * **AWS API Gateway**
 * **AWS CloudFormation**
 * **AWS Lambda**
 * **AWS CloudWatch**
 * **AWS SNS**
 * **AWS DynamoDB**
 * **AWS CodePipeline**
 * **AWS CodeBuild**
 * **AWS CodeDeploy**
 * **AWS CodePipeline**
 * **AWS SecretsManager**

<br />
 <br />

> ## Non AWS Services
 <br />

Below is the list of the Non AWS Services that i have used while deploying my application on AWS:

 * **GitHub**
 * **Pytest**
 
<br />

> ## Getting Started
 <br />

* >### Environment setup
:

To Setup environment of the project:
I used VS Code to write in CDK

```bash
sudo apt udate  >> To update python
sudo apt install python3 python-zip >> To install python
pyhton3 --version >> To check python version
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -0 "awscliv2.zip"
sudo apt install unzip >> To install aws package
unzip awscliv2.zip >> To unzip install package
sudo ./aws/install >> To install aws
aws-version >> To check aws version
```

when the project Setup is complete , we will run the following commands to clone the project
in local AWS environment

```bash
git clone "url-to-github-repo" >> To clone the forked repo
python3 -m venv .venv && source .venv/bin/activate >> To setup virtual environment
pip install -r requirements.aws.txt >> To install requirements
```
### Project Deployment
After the completion of project , the following commands are used in the remote terminal
to deploy the project

```bash
git add .
git commit -m "any"
git push
pytest
cdk synth
aws configure
cdk synth && cdk deploy (name of your pipeline stack wihout commas)
```

* >### Project Deployment
Once the complete code is written and all the requiremnents are fullfilled, i used **CDK Synth** and **CDK Deploy** to create a stack file in Cloud Formation template and then deploying that Cloud Fomation template respectively.

* **CDK Synth:**

    The cdk synth command executes your app, which causes the resources defined in it to be translated into an AWS CloudFormation template. The displayed output of cdk synth is a YAML-format template. The cdk synth command from the CDK CLI generates and prints the CloudFormation equivalent of the CDK stack we've defined.

* **CDK Deploy:**

    The CDK deploy command deploys our CDK stack(s) as CloudFormation template(s). CDK is just an abstraction level above CloudFormation. The whole idea behind CDK is to improve developer experience by allowing us to use a programming language, rather than a configuration language like json or yaml.

* **git add . && git commit -m "" && git push:**

    The **git add .** command adds the current changes to the staging layer, we can revert back if needed from this stage. The **git commit -m ""** command adds the changes from staging to history. The **git push** command pushes the changes from history to github and once the changes are deployed, the AWS stack pipeline will fetch the changes from the **source** and starts to update the entire pipeline automatically.
<br />
<br />


>## Results
In order to display the GUI of multiple services which i have used in my project, my final results and detailed information about the project and end results, please check below-pasted screenshots:


<br />

* #### API Gateway Screenshots

<br />
![image](https://user-images.githubusercontent.com/108882924/209429818-9a351d3d-3494-4a6a-97c8-3f2cec574e1d.png)

![image](https://user-images.githubusercontent.com/108882924/209429843-90e119ef-9745-4891-abcb-bf2c3ebcd9da.png)

![image](https://user-images.githubusercontent.com/108882924/209429861-5b42f1cf-274a-45d4-baf8-714324eb5926.png)





<br />

* #### URL TABLE DYNAMO DB SNAPSHOTS
* 
![image](https://user-images.githubusercontent.com/108882924/209429913-d9e8889a-7006-4478-acc2-293b3dcbc4fc.png)

<br />


<br />

* #### CodePipeline Screenshots
<br />

![image](https://user-images.githubusercontent.com/108882924/209430980-fc2e515c-67c6-49c7-a641-c3b2351a084c.png)

![image](https://user-images.githubusercontent.com/108882924/209430995-605af8f8-5dd6-4d68-91f4-fbef8b967d75.png)



![image](https://user-images.githubusercontent.com/108882924/209430368-174e1ac9-f2f4-468b-9c10-e7b6e366f928.png)



<br />

* #### Docker Pyrest Tests 
* 
![image](https://user-images.githubusercontent.com/108882924/209430023-664cde97-3291-455f-8432-87465f9afe49.png)

![image](https://user-images.githubusercontent.com/108882924/209430056-7fedb330-2b28-4be2-9a45-37976e962ee4.png)


<br />

* #### Unit Functional and Integration Tests
* 
![image](https://user-images.githubusercontent.com/108882924/205709624-7b028a03-e339-4574-acab-0de347edaa32.png)

<br />

> ## Useful Commands

 <br />
Below list contains some of the most handy commands that were used freuently during this project:

```
docker ps -a
docker build -t api-test .
docker run api-test
git add . >> Adds the current changes to staging
git commit -m "" >> Adds the change set in git history
git push >> Pushes the changes to Github Repository
CDK DOC >> Opens cdk documentation
CDK DIFF >> Compare deployed stack with current stack
CDK LS >> List all stacks in the app
CDK DEPLOY >> Deploy the stack on the Cloud
CDK SYNTH >> Emits the synthesized CloudFormation template
```
<br />

> ## References
 <br />

 Below list contains the link for all the references and resources that i have used to build my project:

* [AWS API Gateway](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/README.html)

* [AWS API Reference](https://docs.aws.amazon.com/cdk/api/v2/python/modules.html)

* [AWS SNS Notifications](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns.html)

* [AWS Lambda](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda.html)

* [AWS CloudWatch](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_cloudwatch.html)

* [AWS CodePipeline](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codepipeline.html)

* [AWS CodeBuild](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_codebuild.html)

* [AWS CodeDeploy](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/README.html)

* [AWS Lambda Deployment Groups](https://docs.aws.amazon.com/cdk/api/v1/python/aws_cdk.aws_codedeploy/LambdaDeploymentGroup.html)

* [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/guide/cw-example-using-alarms.html)

* [Pytest](https://docs.pytest.org/en/6.2.x/fixture.html)

<br />

> ## Author Contact
* Name ::Mariam Bhatti
* Email :: mariambhatti8989@gmail.com
* GitHub :: https://github.com/mariam2022skipq/Sirius_Python/tree/main/mariambhatti

 <br />

Thanks for Reading 👍
##### [Back-to-Top](#back-to-top)
