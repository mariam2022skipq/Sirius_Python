# Sirius Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.During this Sprint, we will design nine application specific designs. Some of the designs also need to be developed and deployed as a working solution.


## Design3 TASK 4
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

#### Creating Pipelines

Creating Pipelines through the console is fairly straightforward. This document explains how to perform the following operation on a pipeline with a Lambda Package/Docker Image 
a) Deploy 
b) Maintain
c) Rollbackproduction and connected to many other important components, so minimizing downtime is essential in this case.  


## Question 2: 
### How will you rollback?

Source : 
https://aws.amazon.com/builders-library/automating-safe-hands-off-deployments/#:~:text=Pipelines%20at%20Amazon%20automatically%20validate,underlying%20operation%20system%20(OS).

Metrics monitoring and auto-rollback:
 1) The deployment system actively monitors an alarm to determine if it needs to automatically roll back a deployment.
 2) A rollback will switch the environment back to the container image, AWS Lambda function deployment package, or internal deployment package i.e container images that was previously deployed.
#### Example from Amazon Auto rollback systems:
Each microservice in each Region typically has a high-severity alarm that triggers on thresholds for the metrics that impact the service’s customers (like fault rates and high latency) and on system health metrics (like CPU utilization).This high-severity alarm is used to page the oncall engineer and to automatically roll back the service if a deployment is in progress. Often, the rollback is already in progress by the time the oncall engineer has been paged and starts engaging.
Example : 
ALARM("FrontEndApiService_High_Fault_Rate") OR
ALARM("FrontEndApiService_High_P50_Latency") OR
ALARM("FrontEndApiService_High_Cpu_Usage") 



### Question 3:
### How do you reduce such failures so there is less need to rollback
The best practices to avoid rollbacks is to make smaller deployments and slicing the workload into smaller portions to avoid any issues that come with the implementation of large atomic applications. Moreover, designing applications that are backwards compatible is an important consideration to avoid any issues with existing services. 



## Design Image




## Authors

- [Mariam Bhatti](mariambhatti8989@gmail.com)
