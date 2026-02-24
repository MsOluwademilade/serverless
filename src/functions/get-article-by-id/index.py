import json
import os
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'Articles')
table = dynamodb.Table(table_name)

# Helper function to convert DynamoDB Decimal types to JSON-serializable types
def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")  # Debug logging
    
    # Safely get article_id from pathParameters
    article_id = None
    if event.get('pathParameters') and event['pathParameters']:
        article_id = event['pathParameters'].get('id')
    
    if not article_id:
        return {
            'statusCode': 400,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Missing article ID in path'})
        }
    
    try:
        # Query DynamoDB for the article by ID
        response = table.get_item(Key={'id': article_id})
        
        # Check if the article exists
        if 'Item' not in response:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': f'Article {article_id} not found'})
            }
        
        # Return the article from DynamoDB
        article = response['Item']
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(article, default=decimal_default)
        }
        
    except ClientError as e:
        print(f"Error fetching article: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({'error': 'Internal Server Error'})
        }
