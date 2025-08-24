import boto3
from config.settings import settings

def test_bedrock_access():
    try:
        bedrock = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)
        response = bedrock.list_foundation_models()
        print("✅ AWS Bedrock access successful!")
        print(f"Available models: {len(response['modelSummaries'])}")
        return True
    except Exception as e:
        print(f"❌ AWS Bedrock access failed: {e}")
        print("💡 Check your AWS credentials and region configuration")
        return False

if __name__ == "__main__":
    test_bedrock_access()