
# Sirius Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.


## Task 7 : Design and develop
### What if we have 15MB file that we have to upload on S3 using API gateway. We have the limitation that our API gateway has the maximum payload capacity of 10MB. How you will solve this problem?

### Explaination of the Solution:

To solve this Problem the following steps are followed 
1) AWS services use : API Gateway , AWS lambda, S3 bucket
2) Configure API Gateway and Post method 
3) configure API Gateway with AWS lambda 
4) LAmbda returns the signed URL from S3 bucket to user 
5) User can use this signed URL to upload directly to S3 bucekt
6)API Gateway supports a reasonable payload size limit of 10MB. One way to work within this limit, but still offer a means of importing large datasets to your backend, is to allow uploads through S3. This article shows how to use AWS Lambda to expose an S3 signed URL in response to an API Gateway request. Effectively, this allows you to expose a mechanism allowing users to securely upload data directly to S3, triggered by the API Gateway.


### Design Image
![image](https://user-images.githubusercontent.com/108882924/208077924-f8d91e9d-6fed-451d-a536-2ce00d20c82a.png)

![image](https://user-images.githubusercontent.com/108882924/208078029-6b4f0767-af92-4f11-a15a-fb8ab974d003.png)


The basic flow of the import process is as follows: the user makes an API, which is served by API Gateway and backed by a Lambda function. The Lambda function computes a signed URL granting upload access to an S3 bucket and returns that to API Gateway, and API Gateway forwards the signed URL back to the user. At this point, the user can use the existing S3 API to upload files larger than 10MB.

### API Gateway Results (Getting the signed URL)
![image](https://user-images.githubusercontent.com/108882924/208237764-65ed0b32-ec64-4155-b845-947c7a7b55a8.png)

![image](https://user-images.githubusercontent.com/108882924/208237782-fcbd1103-146d-4ffd-b69e-d0c449b8a588.png)


### Using Postman to send the file to S3 bucket using Pre-signed URL
![image](https://user-images.githubusercontent.com/108882924/208237825-ccc5d0de-3cb4-457b-bcfa-c5942e97dad1.png)



### S3 bucket with Signed URL

![image](https://user-images.githubusercontent.com/108882924/208237898-8c8037f0-30fc-4a18-acfd-8b30fa4301b2.png)



To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```

At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```

To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
