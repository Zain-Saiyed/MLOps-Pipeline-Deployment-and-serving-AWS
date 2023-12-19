import boto3
import json

# Initialize the DynamoDB client
dynamodb = boto3.client(
    'dynamodb',
    region_name=<REGION_NAME>
)

file_to_upload = 'model-metric-data.json'

with open(file_to_upload) as json_file:
    data = json.load(json_file)

# Iterate over each model metrics entry
for item in data:
    metrics = {
        'model_id'  : {'S': item['model_id']},
        'timestamp' : {'S': item['timestamp']},
        'model_type': {'S': item['model_type']},
        'metrics': {
            'M': {
                'accuracy': {'S': str(item['metrics']['accuracy'])},
                'auc_roc': {'S': str(item['metrics']['auc_roc'])},
                'f1_score': {'S': str(item['metrics']['f1_score'])},
                'precision': {'S': str(item['metrics']['precision'])},
                'recall': {'S': str(item['metrics']['recall'])},
                'false_positive': {'S': str(item['metrics']['false_positive'])},
                'true_positive': {'S': str(item['metrics']['true_positive'])},
                'false_negative': {'S': str(item['metrics']['false_negative'])},
                'true_negative': {'S': str(item['metrics']['true_negative'])},
                'support': {'S': str(item['metrics']['support'])}
            }
        }
    }

    if 'training_complete' in item.keys():
        metrics['training_complete'] = {'BOOL': item['training_complete']}
    if 'approved' in item.keys():
        metrics['approved'] = {'BOOL': item['approved']}
    # Put each model metrics entry into the DynamoDB table
    # https://docs.aws.amazon.com/cli/latest/reference/dynamodb/put-item.html
    response = dynamodb.put_item(
        TableName='model_metrics_cf',
        Item=metrics
    )

print("Pushed data successfully to DynamoDB table: 'model_metrics_cf'")