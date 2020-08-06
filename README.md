# ARCAHackathon
> ARCA Hackathon Team anyh0w submission / prototype

> Improving customer satisfaction and staff workload through AWS services for automation and easy access to information.

> ARCA Hackathon, AWS Lambda, Rekognition, SNS, API Gateway




## General Overview of Code

### APIToRDS
- main code that get form infomation from Bizfile+, verifies the data and saves it onto RDS(mySQL)

### getDataFromDashboard
- upon receiving a GET request to API gateway from dashboard, reads data from RDS(mySQL) and returns it to dashboard

### approvalResult
- inputs result of form from Approval officier, and updates database accordingly
- calls sendSNS lambda function to sent notification of result

### sendSNS
- inputs result and phone number, sends a SMS message using AWS SNS

### AWSRekognition
- does text analysis on an image on aws S3

