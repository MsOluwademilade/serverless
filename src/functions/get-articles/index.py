import json

def lambda_handler(event, context):
    # Simulating database fetch, would typically be a DynamoDB query
    articles = [
        {"id": "1", "title": "Article 1", "summary": "Summary of article 1", "published": "2026-02-14"},
        {"id": "2", "title": "Article 2", "summary": "Summary of article 2", "published": "2026-02-14"}
    ]
    
    return {
        'statusCode': 200,
        'body': json.dumps(articles)
    }
