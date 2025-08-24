from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from langchain_aws import BedrockEmbeddings
# from langchain_community.vectorstores import Qdrant
from langchain_qdrant import Qdrant
import boto3
from pydantic import BaseModel
from config.settings import settings

def get_qdrant_client():
    return QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY,
    )

def get_bedrock_embeddings():
    try:
        bedrock_client = boto3.client('bedrock-runtime', region_name=settings.AWS_REGION)
        return BedrockEmbeddings(
            client=bedrock_client,
            model_id='amazon.titan-embed-text-v2:0'
        )
    except Exception as e:
        print(f"Failed to initialize Bedrock embeddings: {e}")
        raise

def create_collection_if_not_exists(qdrant_client, collection_name, vector_size):
    try:
        collection_info = qdrant_client.get_collection(collection_name)
        current_size = collection_info.config.params.vectors.size
        
        if current_size != vector_size:
            print(f"Existing collection has vector size {current_size} but required is {vector_size}")
            print("Recreating collection with new vector size")
            qdrant_client.delete_collection(collection_name)
            raise Exception("Recreate collection")
        else:
            print(f"Collection '{collection_name}' exists (vector size: {vector_size})")
            
    except Exception:
        print(f"Creating collection: {collection_name} with vector size {vector_size}")
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=vector_size,
                distance=Distance.COSINE
            )
        )

def store_documents(documents):
    qdrant_client = get_qdrant_client()
    
    try:
        embeddings = get_bedrock_embeddings()
        test_embedding = embeddings.embed_query("test")
        vector_size = len(test_embedding)
        print(f"Embedding vector size: {vector_size}")
        
        create_collection_if_not_exists(
            qdrant_client,
            settings.COLLECTION_NAME,
            vector_size
        )
        
        vector_store = Qdrant(
            client=qdrant_client,
            collection_name=settings.COLLECTION_NAME,
            embeddings=embeddings
        )
        
        batch_size = 50
        total_docs = len(documents)
        
        for i in range(0, total_docs, batch_size):
            batch = documents[i:i+batch_size]
            vector_store.add_documents(batch)
            print(f"Stored batch {i//batch_size + 1}/{(total_docs-1)//batch_size + 1}")
        
        collection_info = qdrant_client.get_collection(settings.COLLECTION_NAME)
        print(f"Collection Status: {settings.COLLECTION_NAME}")
        print(f"Total points: {collection_info.points_count}")
        print(f"Status: {collection_info.status}")
        
        return vector_store
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
