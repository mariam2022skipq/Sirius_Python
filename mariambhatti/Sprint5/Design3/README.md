# Srius Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.During this Sprint, we will design nine application specific designs. Some of the designs also need to be developed and deployed as a working solution.


## Task 3 -Part1
#### How would you automate deployment (e-g on AWS) for a system that has:
##### a) Source code in a repo
##### b) How do we generate an artifact from the repo that gets published and later is used in some services?
##### c) Are there more than one solutions?


## Tech Stack
##### **Source Control** GitHub
##### **Services** CodePipeline, S3, CodeBuild, ECR

## Solution

### Introduction:
#### What is AWS CI CD pipeline?
CI/CD can be pictured as a pipeline, where new code is submitted on one end, tested over a series of stages (source, build, test, staging, and production), and then published as production-ready code. CICD pipeline overview. Each stage of the CI/CD pipeline is structured as a logical unit in the delivery process.
Containers:


Usually Operating systems like Linux have various processes running in them. These processes share memory/system resources and a common namespace. 

#### Docker Images:
##### *Quoted From Docker*: Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. The service has both free and premium tiers. The software that hosts the containers is called Docker Engine.

#### Amazon ECR (Elastic Container Registry):
Amazon Elastic Container Registry (Amazon ECR) is a fully managed Docker container registry that makes it easy for developers to store, manage, and deploy Docker container images. This allows you to access images from different environments (Prod, Integration stages, etc). 


#### AWS CodeBuild:

##### *Quoted From AWS*: AWS CodeBuild is a fully managed continuous integration service that compiles source code, runs tests, and produces software packages that are ready to deploy. With CodeBuild, you don’t need to provision, manage, and scale your own build servers. CodeBuild scales continuously and processes multiple builds concurrently, so your builds are not left waiting in a queue. You can get started quickly by using prepackaged build environments, or you can create custom build environments that use your own build tools. With CodeBuild, you are charged by the minute for the compute resources you use.

#### Creating Pipelines

Creating Pipelines through the console is fairly straightforward. This document explains how to perform the following operation on a pipeline with a Lambda Package/Docker Image 
a) Deploy 
b) Maintain
c) Rollback

## Code Pipeline 
![image](https://user-images.githubusercontent.com/108882924/206919759-77af4b10-9c21-4870-89ec-50a78fda1227.png)



## How would you automate deployment (e-g on AWS) for a system that has:
#### a) Source code in a repo
##### AWS CI/CD allows complete automation of software deployments, allowing us to deploy reliably and rapidly from repositories hosted on various version control systems or even zip files or artifacts hosted in the S3 bucket or ECR respectively. Codedeploy allows consistent deployment of an application across development, test, and production environments whether deploying to Amazon EC2, AWS Fargate, AWS Lambda, or on-premises servers.
You can use Github or Git commit as a source Repo 

Using AWS codePipeline 
![image](https://user-images.githubusercontent.com/108882924/206923482-3f3c1b2d-b27b-4f13-98cb-016732c22416.png)

![image](https://user-images.githubusercontent.com/108882924/206922183-a0572fcd-e462-44ea-abbe-2e594095b892.png)
Source : https://www.xavor.com/blog/how-to-automate-deployments-on-aws/

#### b) How do we generate an artifact from the repo that gets published and later is used in some services?

Source : https://docs.aws.amazon.com/codepipeline/latest/userguide/welcome-introducing-artifacts.html
https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/aws-properties-codepipeline-pipeline-artifactstore.html

##### CodePipeline creates an Amazon S3 bucket in the same AWS Region to store items for all pipelines. It then uses s3 bucket to store those artifacts.You must have one artifact bucket per Region. If you use the console to create a pipeline or cross-Region actions, default artifact buckets are configured by CodePipeline in the Regions where you have actions.

![image](https://user-images.githubusercontent.com/108882924/206924053-c2e252a1-3d46-4056-be46-9ae6ac957fbc.png)


If you use the AWS CLI to create a pipeline, you can store the artifacts for that pipeline in any Amazon S3 bucket as long as that bucket is in the same AWS account and AWS Region as the pipeline. You might do this if you are concerned about exceeding the limits of Amazon S3 buckets allowed for your account.

![image](https://user-images.githubusercontent.com/108882924/206922386-bbbc7f96-c543-492b-9810-53eae26bbbba.png)


#### c) Are there more than one solutions?
##### To create an artifact other options include using an instance of AWS artifact or AWS codebuild to create a docker image and have it saved to the ECR or S3.
##### Alternatives to codedeploy include:
1) Jenkins
2) Red Hat Ansible Automation Platform
3) Octupus Deploy : Octopus Deploy software is a deployment automation server both on-premises or in the cloud. The software manages QA, acceptance testing and production deployments. Complex deployments steps for .NET, Java, and other platforms are made simple. Manage Access control and measure the performance via Dashboard. Developers, Small and Medium companies make use of the software.
4)Circle CI , GitLab
5) Progress Chef

#### Using Codepipeline with Third-Party action Providers (Github and Jenkins):

![image](https://user-images.githubusercontent.com/108882924/206923217-03657dc7-a766-4bcf-b1b3-334608e68670.png)

#### Use CodePipeLine with ElasticBeanStalk for Continuous Delivery of Web applications to Cloud

https://aws.amazon.com/elasticbeanstalk/
##### Elastic Beanstalk is a compute service that lets you deploy web applications and services to web servers. Use CodePipeline with Elastic Beanstalk for continuous deployment of web applications to your application environment

##### Use CodePipeline with AWS CloudFormation templates for continuous delivery to the cloud


### Technology stack for the whole Pipeline:
![image](https://user-images.githubusercontent.com/108882924/206924136-da09f259-0d75-4d07-be68-891dce4626dc.png)



Source : https://www.trustradius.com/products/aws-codedeploy/competitors



## Design Image
![image](https://user-images.githubusercontent.com/108882924/206924751-5eeff595-c996-4d09-99d8-4efd595d549d.png)





## Authors

- [Mariam Bhatti](mariambhatti8989@gmail.com)

