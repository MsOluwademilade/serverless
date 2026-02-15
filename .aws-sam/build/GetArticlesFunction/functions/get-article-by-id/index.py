import json

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")  # Debug logging
    
    # Safely fetching the article id from the path parameters
    article_id = None
    if 'pathParameters' in event and event['pathParameters']:
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
    
    # Simulating fetching a single article by ID
    article = {
        "id": article_id,
        "title": f"Article {article_id}",
        "content": f"Full content of article {article_id}",
        "published": "2026-02-14"
    }
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(article)
    }
