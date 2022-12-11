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
c) Rollback


## Question 1:
### If the latest Deployment is failing, Why do you think it is ?
Deployments can fail due to a number of reasons but are always triggered when an alarm is raised. A piece of code that is not backwards compatible is also a likely cause of failed deployment.
Despite all these checks, it’s still possible for the deployed code to contain bugs or inconsistencies. The only accurate method of fully certifying that the application or a new feature works according to specification is when a user uses it. Code with a bug may go undetected until it gets to the final user. The code is already in production and connected to many other important components, so minimizing downtime is essential in this case.  


## Question 2: 
### How will you rollback?
Manual rollbacks are not an option on AWS but in case an alarm is triggered, a rollback is initiated automatically. It is important to note that regardless of the deployment technique (Canary, Red-Green Deployment, etc.) applied, the rollback will initiate a new install of the previous working version of the application on all instances. 


### Question 3:
### How do you reduce such failures so there is less need to rollback
The best practices to avoid rollbacks is to make smaller deployments and slicing the workload into smaller portions to avoid any issues that come with the implementation of large atomic applications. Moreover, designing applications that are backwards compatible is an important consideration to avoid any issues with existing services. 



## Design Image




## Authors

- [Mariam Bhatti](mariambhatti8989@gmail.com)
