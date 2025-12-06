from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
from app.config import settings
from app.services.gemini_service import gemini_service
from typing import List, Dict, Any
import logging
import uuid

logger = logging.getLogger(__name__)


class RAGService:
    """Retrieval-Augmented Generation service using Qdrant and Gemini"""
    
    def __init__(self):
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
        )
        self.collection_name = "textbook_content"
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Ensure collection exists"""
        try:
            collections = self.client.get_collections().collections
            if not any(c.name == self.collection_name for c in collections):
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=768, distance=Distance.COSINE),
                )
                logger.info(f"Created collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Collection setup failed: {e}")
    
    async def add_content(
        self,
        text: str,
        metadata: Dict[str, Any]
    ) -> str:
        """Add content chunk to vector database"""
        try:
            # Generate embedding
            embedding = await gemini_service.generate_embedding(text)
            
            # Create point
            point_id = str(uuid.uuid4())
            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "text": text,
                    **metadata
                }
            )
            
            # Upload to Qdrant
            self.client.upsert(
                collection_name=self.collection_name,
                points=[point]
            )
            
            logger.info(f"Added content chunk: {point_id}")
            return point_id
        except Exception as e:
            logger.error(f"Failed to add content: {e}")
            raise
    
    async def search(
        self,
        query: str,
        limit: int = 5,
        filter_metadata: Dict[str, Any] = None
    ) -> List[Dict[str, Any]]:
        """Search for relevant content chunks"""
        try:
            # Generate query embedding
            query_embedding = await gemini_service.generate_query_embedding(query)
            
            # Build filter if provided
            search_filter = None
            if filter_metadata:
                conditions = []
                for key, value in filter_metadata.items():
                    conditions.append(
                        FieldCondition(
                            key=key,
                            match=MatchValue(value=value)
                        )
                    )
                if conditions:
                    search_filter = Filter(must=conditions)
            
            # Search
            results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_embedding,
                limit=limit,
                query_filter=search_filter
            )
            
            # Format results
            formatted_results = []
            for result in results:
                formatted_results.append({
                    "text": result.payload.get("text", ""),
                    "score": result.score,
                    "metadata": {
                        k: v for k, v in result.payload.items() if k != "text"
                    }
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Search failed: {e}")
            raise
    
    async def query(
        self,
        user_query: str,
        user_context: Dict[str, Any] = None,
        chat_history: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Complete RAG pipeline: retrieve + generate"""
        try:
            # Retrieve relevant chunks
            filter_metadata = {}
            if user_context:
                if "module" in user_context:
                    filter_metadata["module"] = user_context["module"]
            
            search_results = await self.search(
                query=user_query,
                limit=5,
                filter_metadata=filter_metadata if filter_metadata else None
            )
            
            # Assemble context
            context_parts = []
            citations = []
            
            for i, result in enumerate(search_results):
                context_parts.append(f"[Source {i+1}] {result['text']}")
                citations.append({
                    "source_number": i + 1,
                    "module": result["metadata"].get("module", "Unknown"),
                    "chapter": result["metadata"].get("chapter", "Unknown"),
                    "section": result["metadata"].get("section", ""),
                    "score": result["score"]
                })
            
            context = "\n\n".join(context_parts)
            
            # Generate response
            response_text = await gemini_service.chat(
                query=user_query,
                context=context,
                chat_history=chat_history
            )
            
            # Calculate confidence based on top score
            confidence = "high" if search_results and search_results[0]["score"] > 0.7 else \
                        "medium" if search_results and search_results[0]["score"] > 0.5 else "low"
            
            return {
                "answer": response_text,
                "citations": citations,
                "confidence": confidence,
                "retrieved_chunks": len(search_results)
            }
        except Exception as e:
            logger.error(f"RAG query failed: {e}")
            raise


# Singleton instance
rag_service = RAGService()
