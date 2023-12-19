import json
import boto3
from PIL import Image
import numpy as np
import io 
import base64
import os

s3_client = boto3.client('s3')

def lambda_handler(event, context):
    
    IMG_WIDTH=IMG_HEIGHT=32
    
    # s3_bucket_name = event['Records'][0]['s3']['bucket']['name']
    # s3_image_obj_key = event['Records'][0]['s3']['object']['key']
    s3_bucket_name=  os.environ['MLOPS_S3_BUCKET_NAME']
    s3_image_obj_key = 'user-uploaded-images/O_14.jpg'
    image_object = s3_client.get_object(Bucket=s3_bucket_name, Key=s3_image_obj_key)
    
    image_data = image_object['Body'].read()
    
    image = Image.open(io.BytesIO(image_data))
    image = image.resize((IMG_WIDTH, IMG_HEIGHT))
    # Normalize image
    image = np.array(image) / 255.0
    image_array = np.expand_dims(image, axis=0)
    base64_encoded_image = base64.b64encode(image_array).decode('utf-8')
    
    return {
        'statusCode': 200,
        'body': json.dumps({'base64_encoded_image': base64_encoded_image})
    }
