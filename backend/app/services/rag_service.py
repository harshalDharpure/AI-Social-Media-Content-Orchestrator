"""
RAG (Retrieval-Augmented Generation) service
"""
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from app.core.vector_store import get_vector_store, get_embeddings
from app.models.schemas import RAGDocument
from typing import List, Dict, Any
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)


class RAGService:
    """Service for RAG operations"""
    
    def __init__(self):
        self.vector_store = None
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
    
    def _get_vector_store(self):
        """Get or initialize vector store"""
        if self.vector_store is None:
            self.vector_store = get_vector_store()
        return self.vector_store
    
    async def add_document(self, content: str, metadata: Dict[str, Any] = None) -> str:
        """Add document to vector store"""
        try:
            # Split document into chunks
            documents = self.text_splitter.create_documents(
                [content],
                metadatas=[metadata or {}]
            )
            
            # Add to vector store
            vector_store = self._get_vector_store()
            ids = [str(uuid.uuid4()) for _ in documents]
            vector_store.add_documents(documents, ids=ids)
            
            logger.info(f"Added {len(documents)} document chunks to vector store")
            return ids[0]
        
        except Exception as e:
            logger.error(f"Error adding document to RAG: {e}")
            raise
    
    async def search(self, query: str, top_k: int = 5) -> str:
        """Search for relevant documents"""
        try:
            vector_store = self._get_vector_store()
            results = vector_store.similarity_search(query, k=top_k)
            
            # Combine results into context
            context = "\n\n".join([doc.page_content for doc in results])
            return context
        
        except Exception as e:
            logger.error(f"Error searching RAG: {e}")
            return ""
    
    async def search_with_metadata(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        """Search for relevant documents with metadata"""
        try:
            vector_store = self._get_vector_store()
            results = vector_store.similarity_search_with_score(query, k=top_k)
            
            documents = []
            for doc, score in results:
                documents.append({
                    "content": doc.page_content,
                    "metadata": doc.metadata,
                    "score": float(score)
                })
            
            return documents
        
        except Exception as e:
            logger.error(f"Error searching RAG with metadata: {e}")
            return []
    
    async def delete_document(self, document_id: str) -> bool:
        """Delete document from vector store"""
        try:
            # Note: This depends on the vector store implementation
            # Some stores may not support deletion
            logger.warning(f"Document deletion not fully implemented for document_id: {document_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting document: {e}")
            return False

