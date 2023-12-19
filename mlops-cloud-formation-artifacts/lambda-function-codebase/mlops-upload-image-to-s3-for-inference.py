import json
import logging 
import base64
import boto3
import os

def lambda_handler(event, context):
    # try:
    request_data = event
    # Get request data
    base64_image = request_data['base64_image']
    uuid_key     = request_data['uuid_key']

    image_data = base64.b64decode(base64_image)

    s3_bucket    = os.environ['MLOPS_S3_BUCKET_NAME']
    s3_image_key = f'user-uploaded-images/{uuid_key}'

    # [PUT] Upload image to S3
    s3 = boto3.client('s3')
    s3.put_object(Body=image_data, Bucket=s3_bucket, Key=s3_image_key)

    return json.dumps({
        'statusCode'   : 200,
        'upload_status': 'success',
        'base64_image' : base64_image,
        'key'          : s3_image_key
    })
