import json
import os
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'Articles')
table = dynamodb.Table(table_name)

# Helper function to convert DynamoDB Decimal types
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")  # Debug logging
    
    try:
        # Scan DynamoDB to get all articles
        response = table.scan()
        articles = response.get('Items', [])
        
        # Handle pagination if there are more items
        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            articles.extend(response.get('Items', []))
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(articles, default=decimal_default)
        }
        
    except ClientError as e:
        print(f"Error fetching articles: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }
