import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    QDRANT_URL = os.getenv("QDRANT_URL", "https://24e64fe8-aed2-4906-8829-5cb41e748f99.us-east-1-0.aws.cloud.qdrant.io:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhY2Nlc3MiOiJtIn0.Ce_nK7lhm__eZ6cZ8dXLT7i_kYvCA7_0v2hLymJBiwA")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "phoenix_content")
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

settings = Settings()