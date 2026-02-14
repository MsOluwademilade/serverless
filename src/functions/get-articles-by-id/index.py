import json

def lambda_handler(event, context):
    # Fetching the article id from the path parameters
    article_id = event['pathParameters']['id']
    
    # Simulating fetching a single article by ID
    article = {
        "id": article_id,
        "title": f"Article {article_id}",
        "content": f"Full content of article {article_id}",
        "published": "2026-02-14"
    }
    
    return {
        'statusCode': 200,
        'body': json.dumps(article)
    }
