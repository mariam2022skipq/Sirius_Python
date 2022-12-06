> SkipQ Sirius: Sprint 5
# Welcome to Design Problem #1!
#### Design Problem - 1: 

<Design & Develop>
Consider that you are getting an event response as {“arg1”: 10} from an API.
Make an AWS app that generates an alarm if arg1 > 10.
When the alarm is raised, send an email to a dummy account.

What will you do if there is no lambda invocation even though the code is working fine and there is no error generated?


##### [Back-to-Top](#back-to-top)
---

## **Table of Contents:**

* ### [Overview](#overview-1)
* ### [Design Diagram](#design-diagram-1)
* ### [CRUD API Gateway](#crud-api-gateway-1)
* ### [Objective](#objective-1)
* ### [AWS Services](#aws-services-1)
* ### [Non AWS Services](#non-aws-services-1)
* ### [Getting Started](#getting-started-1)

    * ### [Environment Setup](#environment-setup-1)

    * ### [Project Setup](#project-setup-1)

    * ### [Project Deployment](#project-deployment-1)

* ### [Results](#results-1)
    
    * ### [API Gateway](#api-gateway-screenshots)

    * ### [DynamoDB](#dynamodb-screenshots)

    * ### [SNS Notifications](#sns-notifications-screenshots)

    * ### [CloudWatch Alarms](#cloudwatch-alarm-screenshots)

 * ### [References](#references-1)
 * ### [Useful Commands](#useful-commands-1)
 * ### [Author Contact](#author-contact-1)

<br />


>  ## Overview
 <br />

This project in order to build a CRUD API Gateway endpoint for the CDK app to populate a ARG DynamoDB table using REST API CRUD operations,in this way, we can monitor the argument values sent by API gateway to a dynamo DB table and do comparison that whether the argument value is greater than threshold of 10. If that is the case ,A cloudwatch alarm is raised and SNS email notification is sent 

 * The ARG1 value metric that I have used to check the integer value sent by API Gateway and is **ARG1 Value Metric**.

 The ARG1 value metric is defined using boto3 SDK and is triggered by a **Lambda Funtion**, which i have converted into a **Cron Job** by defining event rule, which will invoke Lambda after every 60 minutes. This Lambda will then check the values of **ARG1 Values**. Against this metric, i have defined threshold i.e **10 for arg1_value**. If the threshold is breached, An alarm will be triggered in **CloudWatch**. For the momment when alarm is triggered, i have used **AWS SNS Service** to send a detailed notification on subscriber's **Email**, also this SNS will trigger a **Lambda Funtion** which will then save that alarm information in a **DynamoDB Table**.
 
<br />
<br />

>  ## Design Diagram
<br />

![image](https://user-images.githubusercontent.com/108882924/206033886-27e79b80-6864-4478-9d5a-70ccfcff642a.png)



<br />

>  ## CRUD API Gateway
 <br />

 The RESTFUL CRUD API Gateway is implemented by using **AWS API Gateway** which uses the **HTTP** Protocol with the request and response messages to perform the RESTFUL API operations of Create, Read, Update and Delete. From the **AWS API Gateway** i have used the Lambda invoked API Gateway to integrate the API Lambda with the RESTFUL endpoint to perform the following 4 methods:
 <br /> 

 * **GET**
 * **POST**
 * **PATCH**
 * **DELETE**
<br />

The **GET** method performs the functionality to extract all available records using the scan function on the ARG1 DynamoDB table. In case the records are found an **HTTP statusCode:200** is sent along with the scanned data in the body of the **response**. 
<br/>

The **POST** method performs the functionality to send the data in the **request** body to the ARG1 DynamoDB table and upon successful put function an **HTTP statusCode:200** is sent and data is written in the DynamoDB table.
<br />

The **PATCH** method performs the functionality to send a key and reference value to update the existing records value with the sent value using the update function, in response an **HTTP statusCode:200** is sent and data is overwritten in the DynamoDB table for the respective field.
<br />

The **DELETE** method  performs the functionality to delete a record in the table by using the delete function. A key:value pair is sent the request body and upon successful delete operation an **HTTP statusCode:200** is sent and the respective data is deleted in the DynamoDB table.
<br />
<br />

 > ## RESULTS
 <br />
 
![image](https://user-images.githubusercontent.com/108882924/206034492-91a9940a-3c47-4425-8ff4-febf3fd0d633.png)

 <br />
 
 <br />
![image](https://user-images.githubusercontent.com/108882924/206034686-967e8b58-d25e-463f-93d7-b8ac667e3991.png)
<br />

<br />
![image](https://user-images.githubusercontent.com/108882924/206034838-7ee0f6b5-3a33-4826-857a-7435a57fcfb1.png)
<br />

<br />
![image](https://user-images.githubusercontent.com/108882924/206038941-8e47d6c4-ac2d-4748-91f3-3fecbbabd286.png)
<br />

<br />
![image](https://user-images.githubusercontent.com/108882924/206039017-eb8abb27-6df2-48f5-ba8e-461c79d34ee0.png)
<br />

<br />
![image](https://user-images.githubusercontent.com/108882924/206039410-85613768-27cb-40b4-89dd-d9c0846843b6.png)
<br />

<br />
![image](https://user-images.githubusercontent.com/108882924/206039513-4b8a161d-7ef9-4666-af42-e95b9c9201ab.png)
<br />

<br />
![image](https://user-images.githubusercontent.com/108882924/206040669-14831ffb-23b0-4f48-9b09-67fa4fe51fbc.png)
<br />

<br />
![image](https://user-images.githubusercontent.com/108882924/206040709-3f8a0200-443b-4075-b06a-ee639ac89e44.png)
<br />


<br />

> ## AWS-Services
 <br />

 Below is the list of AWS Services that i have used while deploying my application on AWS:

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
In order to use **VS Code** in order to write our code in CDK, first i have setup my environment using below mentioned commands:

```
wsl --install >> To install wsl
```

```
sudo apt udate  >> To update python
sudo apt install python3 python-zip >> To install python
pyhton3 --version >> To check python version
```

```
curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -0 "awscliv2.zip"
sudo apt install unzip >> To install aws package
unzip awscliv2.zip >> To unzip install package
sudo ./aws/install >> To install aws
aws-version >> To check aws version
```
* >### Project setup
Once the environment setup is done, I ran these commands to run project in my local AWS environment:
```
git clone "url-to-github-repo" >> To clone the forked repo
python3 -m venv .venv && source .venv/bin/activate >> To setup virtual environment
pip install -r requirements.aws.txt >> To install requirements
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


> ## Useful Commands

 <br />
Below list contains some of the most handy commands that were used freuently during this project:

```
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
* Name :: Mariam Bhatti
* Email :: mariambhattiskipq@gmail.com
* GitHub :: https://github.com/mariam2022skipq/Sirius_Python/edit/main/mariambhatti/Sprint5/Design1/README.md

 <br />

Thanks for Reading 👍
##### [Back-to-Top](#back-to-top)
