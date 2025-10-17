"""Embedding generation using Sentence Transformers."""
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import uuid
from app.config import settings


class EmbeddingService:
    """Generate and manage embeddings for resumes and jobs."""

    def __init__(self):
        """Initialize embedding service."""
        self.model = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
        self.qdrant_client = QdrantClient(url=settings.QDRANT_URL)
        self._ensure_collection()

    def _ensure_collection(self):
        """Ensure Qdrant collection exists."""
        try:
            self.qdrant_client.get_collection(settings.QDRANT_COLLECTION_NAME)
        except Exception:
            # Collection doesn't exist, create it
            self.qdrant_client.create_collection(
                collection_name=settings.QDRANT_COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=settings.EMBEDDING_SIZE,
                    distance=Distance.COSINE
                )
            )

    def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding vector for text.

        Args:
            text: Input text

        Returns:
            Embedding vector
        """
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()

    def store_resume_embedding(
        self,
        resume_id: int,
        text: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Generate and store resume embedding in Qdrant.

        Args:
            resume_id: Resume database ID
            text: Resume text to embed
            metadata: Additional metadata to store

        Returns:
            Embedding ID in Qdrant
        """
        embedding = self.generate_embedding(text)
        embedding_id = str(uuid.uuid4())

        payload = {
            "resume_id": resume_id,
            "type": "resume",
            **(metadata or {})
        }

        self.qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=[
                PointStruct(
                    id=embedding_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )

        return embedding_id

    def store_job_embedding(
        self,
        job_id: int,
        text: str,
        metadata: Dict[str, Any] = None
    ) -> str:
        """
        Generate and store job embedding in Qdrant.

        Args:
            job_id: Job database ID
            text: Job description text to embed
            metadata: Additional metadata to store

        Returns:
            Embedding ID in Qdrant
        """
        embedding = self.generate_embedding(text)
        embedding_id = str(uuid.uuid4())

        payload = {
            "job_id": job_id,
            "type": "job",
            **(metadata or {})
        }

        self.qdrant_client.upsert(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            points=[
                PointStruct(
                    id=embedding_id,
                    vector=embedding,
                    payload=payload
                )
            ]
        )

        return embedding_id

    def search_similar_jobs(
        self,
        resume_text: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Find similar jobs for a resume using vector search.

        Args:
            resume_text: Resume text
            limit: Number of results to return

        Returns:
            List of matching jobs with scores
        """
        embedding = self.generate_embedding(resume_text)

        results = self.qdrant_client.search(
            collection_name=settings.QDRANT_COLLECTION_NAME,
            query_vector=embedding,
            query_filter={
                "must": [
                    {"key": "type", "match": {"value": "job"}}
                ]
            },
            limit=limit
        )

        matches = []
        for result in results:
            matches.append({
                "job_id": result.payload.get("job_id"),
                "semantic_similarity": result.score,
                "metadata": result.payload
            })

        return matches

    def compute_similarity(self, text1: str, text2: str) -> float:
        """
        Compute cosine similarity between two texts.

        Args:
            text1: First text
            text2: Second text

        Returns:
            Similarity score (0-1)
        """
        emb1 = self.generate_embedding(text1)
        emb2 = self.generate_embedding(text2)

        # Compute cosine similarity
        import numpy as np
        emb1_np = np.array(emb1)
        emb2_np = np.array(emb2)

        similarity = np.dot(emb1_np, emb2_np) / (
            np.linalg.norm(emb1_np) * np.linalg.norm(emb2_np)
        )

        return float(similarity)


# Singleton instance
embedding_service = EmbeddingService()
