# Sirius Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.

## Design 4
#### Design an end-to-end CI/CD delivery pipeline for a website on AWS that has following components: 1) EC2 instances for some static calculations 2) S3 for website pages 3) API GW and lambda triggers 4) CloudWatch alarms on number of API calls received



## Tech Stack
##### **Source Control** AWS S3 Bucket
##### **Services** CodePipeline, S3, CodeBuild, Code Deploy, API Gateway, Lmbda, CloudWatch alarms, Cloud Front , Amazon Cognito , Cloud Trail , Code pipeline components, Amazon EC2, amazon secrets Manager 

## Solution

### Introduction:
#### What is AWS CI CD pipeline?
CI/CD can be pictured as a pipeline, where new code is submitted on one end, tested over a series of stages (source, build, test, staging, and production), and then published as production-ready code. CICD pipeline overview. Each stage of the CI/CD pipeline is structured as a logical unit in the delivery process.
Containers:

#### Creating Pipelines

Creating Pipelines through the console is fairly straightforward. This document explains how to perform the following operation on a pipeline with a Lambda Package/Docker Image 
a) Deploy 
b) Maintain
c) Rollback


## Design Image

![image](https://user-images.githubusercontent.com/108882924/207319492-b6872ca9-0e87-4bed-8697-a56dd110fe9d.png)



![image](https://user-images.githubusercontent.com/108882924/207262098-cf79451c-d28b-4062-a25d-6fbfe48e62fd.png)





### Solution Explained:
##### I have followed the following steps given below for the solution of this design:
#### 1) Set up an Amazon S3 bucket to store the website pages.Also, EC2 instance which can perform static calculations to be required by the website.
#### 2) Continuous Integration and COntinuous Delivery (CI/CD) pipeline is enabled as the Developer pushes the code from a source repo to Codepipeline.
#### 3) For the components of CodePipeline , I have used  CodeCommit , Code build and Code deploy of AWS. Secrets manager is used to retrive token of the repo for pushing code
#### 4) Code is deployed on S3 and EC2.
#### 5) Set up an API Gateway to handle API calls from user and trigger the corresponding Lambda function to retrieve static website content from S3 and EC2 in case of calculations.For example, a Lambda function can be triggered when an API request is received to retrieve data from the EC2 instance and return it to the website.
#### 6) Amazon Cloudwatch is configured with lambda and it can also be directly connected with API Gateway to trigger a CloudWatch Alarms on the number of API calls recieved.
#### 7)There is another solution for accessing static website content. CloudFront distribution can be used for accessing content from S3 by the user using Signed URLs
#### 8) Amazon Cognito is used for user authentication using congito user pools
#### 9) Amazon CloudTrail can also be enabled to watch the codepipeline events and API calls and other AWS account Events and sends them to Cloudwatch logs





- [Mariam Bhatti](https://github.com/mariam2022skipq/Sirius_Python)
