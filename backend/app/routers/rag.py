"""
RAG (Retrieval-Augmented Generation) router
"""
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.models.schemas import RAGUploadRequest, RAGDocument
from app.services.rag_service import RAGService
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

router = APIRouter()
rag_service = RAGService()


@router.post("/upload")
async def upload_document(request: RAGUploadRequest):
    """Upload document to RAG"""
    try:
        document_id = await rag_service.add_document(
            content=request.content,
            metadata=request.metadata or {}
        )
        return {"document_id": document_id, "message": "Document uploaded successfully"}
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/upload/file")
async def upload_file(file: UploadFile = File(...)):
    """Upload file to RAG"""
    try:
        content = await file.read()
        content_str = content.decode("utf-8")
        
        document_id = await rag_service.add_document(
            content=content_str,
            metadata={"filename": file.filename, "content_type": file.content_type}
        )
        return {"document_id": document_id, "message": "File uploaded successfully"}
    except Exception as e:
        logger.error(f"Error uploading file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/search")
async def search_documents(query: str, top_k: int = 5):
    """Search documents in RAG"""
    try:
        results = await rag_service.search_with_metadata(query, top_k)
        return {"query": query, "results": results}
    except Exception as e:
        logger.error(f"Error searching documents: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/document/{document_id}")
async def delete_document(document_id: str):
    """Delete document from RAG"""
    try:
        success = await rag_service.delete_document(document_id)
        if success:
            return {"message": "Document deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        logger.error(f"Error deleting document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

