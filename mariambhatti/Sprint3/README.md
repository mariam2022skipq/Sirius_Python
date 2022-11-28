# Project Title

## CI/CD project : Create multi-stage code pipeline having Beta/Gamma and Prod stage using AWS CDK and auto deployment

## **Table of Contents:**

* ### [Overview](#overview-1)
* ### [Project Steps and deployment](#project-Steps-and-deployment-1)
* ### [Results of the Project](#Results-of-the-project-1)
* ## [Useful Commands](#Useful-commands-1)
* ## [References](#References-1)
* ## [AWS services used in this Project](#AWS-services-used-in-the-project-1)



### Overview

In this project, I have built Contains a CI/CD pipeline which will pull my code from the GitHub repository, build my code, run tests on my code and then deploy it to production. This CI/CD pipeline will help me speed up my development by automating all the necessary steps to push code in production. It is a multi-stage pipeline having Beta/Gamma and Prod stage using CDK. Each stage has BakeTimes, code-reviews and test blockers.Unit tests and functional tests are also added.Stages are also linked with AWS CloudWatch Metrics and alarms for the operational Health of web Crawler, including memory and time-to-process each crawler run. Automatic rollback is also enabled if metrics are in alarm. Automatic unit testng and functional testing is enabled using Pytest.There is a setup of Setup beta and prod environments in CodePipeline and deploy using CodeDeploy


Following are the main tasks/steps of the project:

1)Create a web health crawler with that monitors the web health using implementation of AWS services like Lambda, DynamoDb , SNS , Cloudwatch
2) Creation of CI/CD pipeline : AWS code commit and AWS code build
3) Adding stages to Pipeline (Beta and Prod) : shell step
4) Adding Unit tests , Functional and Integration tests
5) Adding Unit test step in beta stage and approval step before Prod stage
6) Creating metrics for Webcrawler(Checking health of lambda functions) and creating alarms on the metrics
7) Configure Auto rollbacks if metrics are in alarm




## Project execution and Deployment

### Environemnt Setup

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


### CI/CD Process

![process](https://user-images.githubusercontent.com/108882924/204315658-d3d9dda3-fe6c-4804-ac19-af30f9725fc1.png)


### My CI/CD pipeline
![image](https://user-images.githubusercontent.com/108882924/204316105-aa0e47e6-9835-4b3c-8c01-6584804de9bb.png)
![image](https://user-images.githubusercontent.com/108882924/204316443-1c3923f1-1f6e-4581-a9ec-64cc22c6db4f.png)

### Cloudwatch metrics
![image](https://user-images.githubusercontent.com/108882924/204317360-1df8240c-81ef-4790-9006-decf12e08e3c.png)



### Running testcases (Pytest results)
![image](https://user-images.githubusercontent.com/108882924/204317677-aa55ed21-9a2c-42d3-b15a-0ef3731be25d.png)


### Dynamo Db entries 
![image](https://user-images.githubusercontent.com/108882924/204317862-883359fb-5895-4cdd-bc02-ca706448efd8.png)


> ## Useful Commands
<br />
Below list contains some of the most handy commands that were used freuently during this project:
```
CDK DOC >> Opens cdk documentation
CDK DIFF >> Compare deployed stack with current stack
CDK LS >> List all stacks in the app
CDK DEPLOY >> Deploy the stack on the Cloud
CDK SYNTH >> Emits the synthesized CloudFormation template
```
<br />

> ## References
<br />
Below is the link for all the references and resources that i have used to build my project:
* [AWS API Reference](https://docs.aws.amazon.com/cdk/api/v2/python/modules.html)
* [AWS Lambda](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_lambda.html)
* [AWS SNS Notifications](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns.html)
* [AWS SNS](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_sns.html)
* [AWS Events](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_events.html)

<br />

## AWS services used in this Project

The following AWS services are being used for this project :
1) AWS Lambda 
2) AWS CloudWatch
3) AWS SNS
4) Dynamo DB
5) AWS Code pipeline

## 🚀 About Me
I'm a Software Developer Turning devops enginner
Email :mariambhatti8989@gmail.com
<br />
Thanks for Reading 👍

