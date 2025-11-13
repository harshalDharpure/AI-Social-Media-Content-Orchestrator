"""
Vector store initialization for RAG pipeline
"""
from langchain.vectorstores import Pinecone, Qdrant
from langchain_openai import OpenAIEmbeddings
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
import pinecone
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Global vector store
vector_store = None
embeddings: Embeddings = None


def init_vector_store():
    """Initialize vector store (Pinecone or Qdrant)"""
    global vector_store, embeddings
    
    try:
        # Initialize embeddings
        if settings.OPENAI_API_KEY:
            embeddings = OpenAIEmbeddings(openai_api_key=settings.OPENAI_API_KEY)
            logger.info("Using OpenAI embeddings")
        else:
            # Fallback to HuggingFace embeddings
            embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )
            logger.info("Using HuggingFace embeddings")
        
        if settings.USE_PINECONE and settings.PINECONE_API_KEY:
            # Initialize Pinecone
            pinecone.init(
                api_key=settings.PINECONE_API_KEY,
                environment=settings.PINECONE_ENVIRONMENT
            )
            
            # Create index if it doesn't exist
            if settings.PINECONE_INDEX_NAME not in pinecone.list_indexes():
                pinecone.create_index(
                    name=settings.PINECONE_INDEX_NAME,
                    dimension=1536 if settings.OPENAI_API_KEY else 384,
                    metric="cosine"
                )
            
            vector_store = Pinecone.from_existing_index(
                index_name=settings.PINECONE_INDEX_NAME,
                embedding=embeddings
            )
            logger.info("Pinecone vector store initialized")
        
        else:
            # Initialize Qdrant
            qdrant_client = QdrantClient(
                url=settings.QDRANT_URL,
                api_key=settings.QDRANT_API_KEY if settings.QDRANT_API_KEY else None
            )
            
            # Create collection if it doesn't exist
            try:
                qdrant_client.get_collection("social_media_content")
            except:
                qdrant_client.create_collection(
                    collection_name="social_media_content",
                    vectors_config=VectorParams(
                        size=1536 if settings.OPENAI_API_KEY else 384,
                        distance=Distance.COSINE
                    )
                )
            
            vector_store = Qdrant(
                client=qdrant_client,
                collection_name="social_media_content",
                embeddings=embeddings
            )
            logger.info("Qdrant vector store initialized")
    
    except Exception as e:
        logger.error(f"Failed to initialize vector store: {e}")
        raise


def get_vector_store():
    """Get vector store instance"""
    if vector_store is None:
        init_vector_store()
    return vector_store


def get_embeddings():
    """Get embeddings instance"""
    if embeddings is None:
        init_vector_store()
    return embeddings

