# Sirius Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.During this Sprint, we will design nine application specific designs. Some of the designs also need to be developed and deployed as a working solution.


## Design3 TASK 2
Design & Develop - Deploy, maintain and rollback pipeline for an artifact deployment e-g lambda
package, docker image etc.
##### 1) If the latest Deployment is failing, Why do you think it is ?
##### 2) How will you rollback?
##### 3) How do you reduce such failures so there is less need to rollback

## Tech Stack
##### **Source Control** GitHub
##### **Services** CodePipeline, CloudFormation, CodeBuild, ECR, EC2

## Solution

### Introduction:
#### What is AWS CI CD pipeline?
CI/CD can be pictured as a pipeline, where new code is submitted on one end, tested over a series of stages (source, build, test, staging, and production), and then published as production-ready code. CICD pipeline overview. Each stage of the CI/CD pipeline is structured as a logical unit in the delivery process.
Containers:


Usually Operating systems like Linux have various processes running in them. These processes share memory/system resources and a common namespace. 

#### Docker Images:
##### *Quoted From Docker*: Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. The service has both free and premium tiers. The software that hosts the containers is called Docker Engine.

Amazon ECR (Elastic Container Registry):
Amazon Elastic Container Registry (Amazon ECR) is a fully managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images. This allows you to access images from different environments (Prod, Integration stages, etc). 


#### AWS CodeBuild:

##### *Quoted From AWS*: AWS CodeBuild is a fully managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy. With CodeBuild, you don’t need to provision, manage, and scale your own build servers. CodeBuild scales continuously and processes multiple builds concurrently, so your builds are not left waiting in a queue. You can get started quickly by using prepackaged build environments, or you can create custom build environments that use your own build tools. With CodeBuild, you are charged by the minute for the compute resources you use.

#### AWS CodeDeploy
####  CodeDeploy is a deployment service that automates application deployments to Amazon EC2 instances, on-premises instances, serverless Lambda functions, or Amazon ECS services.CodeDeploy can deploy application content that runs on a server and is stored in Amazon S3 buckets, GitHub repositories, or Bitbucket repositories. CodeDeploy can also deploy a serverless Lambda function. You do not need to make changes to your existing code before you can use CodeDeploy.

#### Creating Pipelines

Creating Pipelines through the console is fairly straightforward. This document explains how to perform the following operation on a pipeline with a Lambda Package/Docker Image 
a) Deploy 
b) Maintain
c) Rollbackproduction and connected to many other important components, so minimizing downtime is essential in this case.  

## Question 1:
### if the latest deployment is failing, why do you think that is?
Source:https://docs.aws.amazon.com/codedeploy/latest/userguide/troubleshooting-deployments.html
#### General troubleshooting Deployment Failure issues :
1) Codedeploy deployment resources are supported in only some AWS regions
2) Required IAM roles are not available :If you rely on an IAM instance profile or a service role that was created as part of an AWS CloudFormation stack, if you delete the stack, all IAM roles are deleted, too.
#### Deployment Failures due to EC2 instances / on -prem Deployment

![image](https://user-images.githubusercontent.com/108882924/206914329-f2bb86f3-c84f-4494-8ff4-9e8ae541e12e.png)

3) Sometimes the Blue/Green Deployment fails due to Allow Traffic Lifecycle event : incorrectly configured health checks in Elastic Load Balancing used to manage traffic to the deployment group
4) AWS Lambda deployments fail after manually stopping a Lambda deployment that doesnot have configured rollbacks: the alias of lambda Function specified in deployment might refence two different versions of the function therefor subsequent attempts to
5) Tagging an instance as a part of a deployment group does not automatically deploy your application to a new instance 
6) Invalid GitHub OAuth token



## Question 2: 
### How will you rollback?

Source : 
https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/#:~:text=Pipelines%20at%20Amazon%20automatically%20validate,underlying%20operation%20system%20(OS).

Metrics monitoring and auto-rollback:
 1) The deployment system actively monitors an alarm to determine if it needs to automatically roll back a deployment.
 2) A rollback will switch the environment back to the container image, AWS Lambda function deployment package, or internal deployment package i.e container images that was previously deployed.
 3) You can also Manually Configure deployment rollback in the CDK code 
#### Example from Amazon Auto rollback systems:
Each microservice in each Region typically has a high-severity alarm that triggers on thresholds for the metrics that impact the service’s customers (like fault rates and high latency) and on system health metrics (like CPU utilization).This high-severity alarm is used to page the oncall engineer and to automatically roll back the service if a deployment is in progress. Often, the rollback is already in progress by the time the oncall engineer has been paged and starts engaging.
Example : 
ALARM("FrontEndApiService_High_Fault_Rate") OR
ALARM("FrontEndApiService_High_P50_Latency") OR
ALARM("FrontEndApiService_High_Cpu_Usage") 



### Question 3:
### How do you reduce such failures so there is less need to rollback
1) More testing phases More types of testing : Unit , functional , Integration tests
2) Multpile Pre-production environments such as gamma stage: Gamma validates that the code is both functional and that it can be safely deployed to production. Gamma is as production-like as possible, including the same deployment configuration, the same monitoring and alarms, and the same continuous canary testing as production. Gamma is also deployed in multiple AWS Regions to catch any potential impact from regional differences. 
3) Use autorollback configuration
4) Limiting the scope of each individual deployment limits the potential impact on customers from failed production deployments and prevents a multi-Availability-Zone or multi-Region ,impact split the production phase of the pipeline into many stages and many deployments to individual Regions

![image](https://user-images.githubusercontent.com/108882924/206913013-a6b3d8f0-d7b2-49ab-bc21-67729d3f75e8.png)

### Code pipeline 



## Design Image

![image](https://user-images.githubusercontent.com/108882924/206924895-d0a4b961-f752-4600-9757-4b808d6406a6.png)


![image](https://user-images.githubusercontent.com/108882924/206919512-04c8b02f-1f14-43b9-bf09-d5baf80d8e90.png)

## Code Pipeline

![image](https://user-images.githubusercontent.com/108882924/206919622-b315ec4d-eeb4-4f5c-bf43-b150af56e07c.png)





## Author

- [Mariam Bhatti](mariambhatti8989@gmail.com)
