# Pegasus Python Sprint 5

Sprint 5 is a series of tasks that entail various challenges designed to allow the trainee to build on existing and new knowledge of the AWS platform and develop/design solutions.

## Task 5
#### Design & Develop - Suppose there are 10 files uploading to S3 bucket each day. For each file received on cloud storage, you have a mechanism to process the file. During the processing, your code parses the text and counts the number of times each word is repeated in the file. For example, in the following text: “Hello World and Hello There”, your code should be able to say that "hello" has been used twice, "world" has occured once and so on. Then it will store the results in some storage and email to some email address after successful processing.


## Tech Stack
##### **Source Control** AWS S3 Bucket
##### **Services** S3, LAmbda, SES

## Solution 

##### In order to solve this problem, a simple solution was adopted that required using S3 bucket or the object storage and then triggering lambda Event notifications. Once done, this allows us to create entries in the Dynamo table and also send an email to a specific email address via SES

### Result:

#### Input string:
“Hello World and Hello There”

#### Output string:
{'Hello': 2, 'World': 1, 'and': 1,  'there': 1}
## Design Images
##Design Screenshot

![image](https://user-images.githubusercontent.com/108882924/207578789-1f6a1e3a-da62-4a05-9afe-d873376e2dd7.png)


##S3 Bucket
![image](https://user-images.githubusercontent.com/108882924/207579000-5d4106ea-e961-4463-b8cd-7df614e4bcae.png)



##S3 Upload Triggred Invocations
![App Screenshot](https://i.imgur.com/ygSJgMK.png)

##Database Screenshot
![image](https://user-images.githubusercontent.com/108882924/207579759-ca04e080-33e3-4ae0-88c4-231777c85153.png)

![image](https://user-images.githubusercontent.com/108882924/207579505-7568c94d-2151-4757-9835-a22ce303dd0e.png)




## Author

- mariam bhatti
-mariambhatti8989@gmail.com
