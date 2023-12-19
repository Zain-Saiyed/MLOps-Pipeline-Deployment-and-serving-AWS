import json
import boto3
import os
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    timestamp = event["timestamp"]
    # timestamp = "21112023231415"
    s3_bucket_name =  os.environ['MLOPS_S3_BUCKET_NAME']
    # model artifact folder to delete
    prefix = f"model_artifacts/cnn-sagemaker-model-training-job-{timestamp}/"
    # Get list of all objects in the prefix
    objects_to_delete = s3_client.list_objects_v2(Bucket=s3_bucket_name, Prefix=prefix)
    delete_keys = {'Objects': [{'Key': s3_obj['Key']} for s3_obj in objects_to_delete.get('Contents', [])]}
    if delete_keys['Objects']:
        s3_client.delete_objects(Bucket=s3_bucket_name, Delete=delete_keys)
    
    # Reset the dynamodb table data    
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1') 

    table_name = os.environ['MLOPS_DYNAMODB_TABLE']
    table = dynamodb.Table(table_name)
    item = {
        "model_id": "model-staged",
        "timestamp": None,
        "model_type": "latest-staged",
        "training_complete": None,
        "approved": None,
        "metrics": {
          "auc_roc": None,
          "f1_score": None,
          "false_positive": None,
          "true_positive": None,
          "false_negative": None,
          "true_negative": None,
          "accuracy": None,
          "precision": None,
          "recall": None,
          "support": None
        }   
    }
    # Update table values
    table.put_item(Item=item)
    
    # Send SNS email notifyng the reejction status to subscribers
    email_subject = "[NOTIFICATION] Latest staged model rejected"
    email_message = "Model artifacts for latest staged model was rejected.\n\n"
    email_message += "Timestamp of model = "+timestamp+"\n\n"

    # Publish message to SNS
    sns = boto3.client('sns', region_name='us-east-1')
    topic_name = os.environ['SNSTopicName']
    topic_arn = 'arn:aws:sns:us-east-1:977687782973:'+topic_name
    response = sns.publish(
        TopicArn=topic_arn,
        Subject=email_subject,
        Message=email_message
    )

    return {
        'statusCode': 200,
        'body': json.dumps('Model Rejected!')
    }

