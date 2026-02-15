import json

def lambda_handler(event, context):
    print(f"Event: {json.dumps(event)}")  # Debug logging
    
    # Simulating database fetch, would typically be a DynamoDB query
    articles = [
        {"id": "1", "title": "Article 1", "summary": "Summary of article 1", "published": "2026-02-14"},
        {"id": "2", "title": "Article 2", "summary": "Summary of article 2", "published": "2026-02-14"}
    ]
    
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(articles)
    }
