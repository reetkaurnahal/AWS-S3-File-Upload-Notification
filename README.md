# AWS-S3-File-Upload-Notification
# AWS S3 File Upload Notification POC

## Overview

This project demonstrates an event-driven notification system using AWS services. Whenever a new file is uploaded to an Amazon S3 bucket, an event triggers an AWS Lambda function that processes the upload event and sends an email notification through Amazon SNS.

The project was implemented as a hands-on AWS Proof of Concept (POC) to understand event-driven architecture, serverless computing, IAM permissions, monitoring, and automated notifications.

## Architecture

**Workflow:**

1. A user uploads a file to an Amazon S3 bucket.
2. Amazon S3 detects the object creation event.
3. S3 invokes the AWS Lambda function.
4. Lambda extracts the uploaded file details.
5. Lambda publishes a notification to an Amazon SNS topic.
6. Amazon SNS sends an email notification to the subscribed email address.
7. Amazon CloudWatch stores Lambda logs and provides monitoring metrics.

## AWS Services Used

| Service | Purpose |
|---|---|
| Amazon S3 | Stores uploaded files and generates object creation events |
| AWS Lambda | Processes S3 events and prepares notifications |
| Amazon SNS | Delivers email notifications |
| AWS IAM | Controls permissions between AWS services |
| Amazon CloudWatch | Stores Lambda logs and monitors execution |

## Architecture Flow

```text
             User Uploads File
                    |
                    v
              Amazon S3
           (Object Created)
                    |
                    v
             AWS Lambda
       (Process Upload Event)
                    |
                    v
               Amazon SNS
                    |
                    v
          Email Notification
                    |
                    v
              User Inbox

        CloudWatch Logs & Metrics
        (Monitoring and Debugging)
```

## Implementation

### 1. Create an S3 Bucket

- Created an S3 bucket in the AWS Mumbai Region (`ap-south-1`).
- Used the bucket to store uploaded files.
- Configured the bucket to generate notifications for object creation events.

### 2. Create an SNS Topic

- Created an Amazon SNS topic.
- Added an email subscription.
- Confirmed the subscription through the confirmation email.

### 3. Configure IAM Permissions

Created an IAM role for Lambda with:

- `AWSLambdaBasicExecutionRole` for CloudWatch logging.
- A custom IAM policy allowing `sns:Publish` on the specific SNS topic.

Permissions were restricted to the required SNS resource.

### 4. Create the Lambda Function

Created a Python Lambda function named:

`S3UploadNotificationFunction`

The function:

- Receives the S3 event.
- Extracts the bucket name and uploaded file key.
- Extracts the event name and AWS Region.
- Constructs a notification message.
- Publishes the message to SNS.

### 5. Configure Environment Variable

Configured the following Lambda environment variable:

```text
SNS_TOPIC_ARN=<your-sns-topic-arn>
```

This avoids hardcoding the SNS topic ARN in the Lambda source code.

### 6. Configure the S3 Event Trigger

Configured the S3 bucket to invoke Lambda for:

- All object creation events.

No prefix or suffix filters were configured during the POC.

### 7. Test the Solution

Uploaded test files to the S3 bucket and verified that:

- S3 generated an object creation event.
- Lambda was invoked successfully.
- Lambda processed the event.
- SNS published the notification.
- The email notification was received.
- Lambda execution logs were available in CloudWatch.

## Lambda Function

The Lambda function source code is available in the `lambda/` directory.

## Sample Notification

```text
Subject: New File Uploaded to S3

A new file has been uploaded to your S3 bucket.

Bucket Name: <bucket-name>

File Name: <uploaded-file-name>

Event: ObjectCreated:Put

Region: ap-south-1

File Location:
s3://<bucket-name>/<uploaded-file-name>
```

## Monitoring and Troubleshooting

Amazon CloudWatch was used to:

- View Lambda execution logs.
- Verify successful function invocations.
- Inspect processed S3 event details.
- Troubleshoot errors.
- Monitor Lambda invocation and error metrics.

## Key Learnings

- Event-driven architecture in AWS.
- S3 event notifications.
- Serverless application development using AWS Lambda.
- Integrating AWS services using IAM roles.
- Publishing messages using Amazon SNS.
- Lambda environment variables.
- CloudWatch Logs and monitoring.
- AWS least-privilege permissions.

## Security Considerations

For a production implementation:

- Keep the S3 bucket private.
- Follow the principle of least privilege.
- Restrict SNS publishing permissions to the required topic.
- Avoid exposing AWS account IDs, credentials, or sensitive information.
- Consider server-side encryption for stored objects.
- Configure CloudWatch log retention.
- Consider duplicate event handling and failure handling.
- Implement monitoring and alerting for Lambda failures.

## Future Enhancements

- Add S3 prefix and suffix filters.
- Generate pre-signed URLs for secure file downloads.
- Add an Amazon SQS queue for improved reliability.
- Configure a dead-letter queue or failure destination.
- Add CloudWatch alarms for Lambda failures.
- Implement infrastructure deployment using AWS CloudFormation or Terraform.
- Improve notification formatting.

## Project Status

**Completed – Successfully tested using file uploads and email notifications.**

This project was implemented as a hands-on AWS POC for learning and experimentation.
