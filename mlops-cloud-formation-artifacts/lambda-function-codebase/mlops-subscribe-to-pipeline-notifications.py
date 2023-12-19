import json
import boto3
import logging
import os

def lambda_handler(event, context):
    # Create SNS client
    sns_client = boto3.client('sns')
    topic_name = os.environ['SNSTopicName']
    topic_arn = 'arn:aws:sns:us-east-1:977687782973:'+topic_name
    try:
        email_id = event['email_id'] 
        # email_id = event['body']['email_id'] 
    
        sns_client.subscribe(
            TopicArn = topic_arn,
            Protocol = 'email',
            Endpoint = email_id
        )
        status = True
    except Exception as e:
        logging.error('error : '+str(e))
        status = False        

    return json.dumps({
        'statusCode': 200,
        'body': { 
            "message": "accepted" if status else "rejected",
            'status' : status
        }
    })
