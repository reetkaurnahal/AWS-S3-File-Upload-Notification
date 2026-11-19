import json
import boto3
import urllib.parse
import os

# Initialize SNS client
sns = boto3.client('sns')

# Read SNS Topic ARN from Lambda environment variable
SNS_TOPIC_ARN = os.environ['SNS_TOPIC_ARN']


def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event))

    for record in event['Records']:

        # Extract S3 bucket name
        bucket_name = record['s3']['bucket']['name']

        # Decode uploaded file name
        object_key = urllib.parse.unquote_plus(
            record['s3']['object']['key']
        )

        # Extract event details
        event_name = record['eventName']
        region = record['awsRegion']

        # Construct S3 file location
        file_location = f"s3://{bucket_name}/{object_key}"

        # Email subject
        subject = "New File Uploaded to S3"

        # Construct email message
        message = f"""
A new file has been uploaded to your S3 bucket.

Bucket Name: {bucket_name}

File Name: {object_key}

Event: {event_name}

Region: {region}

File Location:
{file_location}
"""

        # Publish notification to SNS
        response = sns.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )

        print("SNS notification sent successfully")
        print("SNS Message ID:", response['MessageId'])

    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent successfully')
    }
