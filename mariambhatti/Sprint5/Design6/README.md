# Sirius Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.

## Task 6
#### Client needs a Notification System – that notifies the Admins about report summaries, users about operations within the system, notifying clients/users about any changes. What AWS service(s) would you use for such a system?
 


## Tech Stack
##### **Services** S3, CLOUDWATCH , SnS, aurora, SNS, QUICKSIGHT, Event Bridge, Lambda , Guard duty

## Solution 

##### I am assuming that there are 3 stakeholder in this system . 1) Client 2) User 3) Admin.. Client and Users need notifications of any operational changes in the system

### Required: Summaries of Reports to Admin

##### Application data is sent by eventBridge to Aurora and it can be connected to AWS QuickSIght to provide summary reports 

### Required: Changes Notification

##### EventBrige is connected to Cloudformation which is also connected to cloudwatch and it sends changes notification to users and clients when a lambda is triggered through SNS notifications


### Design Screenshot
 
![image](https://user-images.githubusercontent.com/108882924/207843185-e0ef43a6-f785-4fda-aaaa-73ed90807e1d.png)



## Authors

- Mariam Bhatti
- mariambhatti8989@gmail.com
