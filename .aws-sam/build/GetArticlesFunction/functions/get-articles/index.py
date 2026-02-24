import json
import os
import boto3
from decimal import Decimal
from botocore.exceptions import ClientError

# Initialize the DynamoDB client
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'Articles')
index_name = os.environ.get('INDEX_NAME', 'CategoryPublishedIndex')
table = dynamodb.Table(table_name)

# Helper class to handle DynamoDB Decimal types
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj) if obj % 1 == 0 else float(obj)
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    print(f"Event received: {json.dumps(event, default=str)}")
    
    # Get query parameters
    query_params = event.get('queryStringParameters', {}) or {}
    category = query_params.get('category', 'general')  # Default to 'general' category
    limit = int(query_params.get('limit', '20'))  # Default 20 articles
    last_key = query_params.get('lastKey')  # For pagination
    
    try:
        # Use Query on GSI instead of Scan
        query_kwargs = {
            'IndexName': index_name,
            'KeyConditionExpression': 'category = :category',
            'ExpressionAttributeValues': {
                ':category': category
            },
            'Limit': limit,
            'ScanIndexForward': False  # Sort by published date descending (newest first)
        }
        
        # Handle pagination
        if last_key:
            try:
                query_kwargs['ExclusiveStartKey'] = json.loads(last_key)
            except json.JSONDecodeError:
                print(f"Invalid lastKey format: {last_key}")
        
        print(f"Querying index {index_name} for category: {category}")
        response = table.query(**query_kwargs)
        
        articles = response.get('Items', [])
        print(f"Found {len(articles)} articles")
        
        # Build response with pagination support
        result = {
            'articles': articles,
            'count': len(articles),
            'category': category
        }
        
        # Include pagination token if there are more results
        if 'LastEvaluatedKey' in response:
            result['nextKey'] = json.dumps(response['LastEvaluatedKey'], cls=DecimalEncoder)
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(result, cls=DecimalEncoder)
        }
        
    except ClientError as e:
        print(f"DynamoDB ClientError: {e}")
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'details': f'{error_code}: {error_message}'
            })
        }
    except Exception as e:
        print(f"Unexpected error: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal Server Error',
                'details': str(e)
            })
        }
