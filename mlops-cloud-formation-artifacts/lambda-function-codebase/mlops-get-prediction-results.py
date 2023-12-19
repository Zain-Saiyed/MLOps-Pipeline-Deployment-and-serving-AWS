import json
import boto3
import base64

runtime = boto3.client('sagemaker-runtime')

def lambda_handler(event, context):
    # Get the base 64 image from json payload
    base64_encoded_image = event['base64_encoded_image']
    
    image_bytes = base64.b64decode(base64_encoded_image)    
    payload = json.dumps({'instances': [{'b64': image_bytes.decode('utf-8')}]})

    endpoint_name = "cnn-serverless-endpoint"
    # Invoke the SageMaker endpoint to get prediction on the user's image 
    response = runtime.invoke_endpoint(
        EndpointName = endpoint_name,
        ContentType  = 'application/json',
        Body         = payload
    )
    prediction_probability = json.loads(response['Body'].read().decode())
    
    return {
        'statusCode': 200,
        'prediction_probability': json.dumps(prediction_probability)
    }

