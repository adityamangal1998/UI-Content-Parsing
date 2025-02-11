import boto3
import json
import config

# Initialize AWS session
session = boto3.Session(
    aws_access_key_id=config.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
    region_name=config.AWS_REGION_NAME
)

# Initialize Bedrock runtime client
bedrock_runtime = session.client('bedrock-runtime')

def invoke_model_api(prompt_text):
    """Invokes the Bedrock API with the given prompt text."""
    kwargs = {
        "modelId": config.BEDROCK_MODEL_ID,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "inferenceConfig":{
                "max_new_tokens": 800,
                "top_p": 0.9,
                "top_k": 15,
                "temperature": 0.4
            },
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt_text,
                        }
                    ]
                }
            ]
        })
    }

    response = bedrock_runtime.invoke_model(**kwargs)
    generated_text = json.loads(response['body'].read().decode('utf-8'))
    return generated_text['output']['message']['content'][0]['text']