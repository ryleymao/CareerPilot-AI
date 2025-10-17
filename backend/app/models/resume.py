"""Resume model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Resume(Base):
    """Resume model."""

    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)

    # Raw text content
    raw_text = Column(Text, nullable=False)

    # Parsed structured data
    parsed_data = Column(JSON, nullable=True)  # Full structured resume data

    # Extracted fields for quick access
    skills = Column(JSON, nullable=True)  # List of skills
    experience_years = Column(Integer, nullable=True)
    education = Column(JSON, nullable=True)  # List of education entries
    work_experience = Column(JSON, nullable=True)  # List of work experience entries

    # Embedding for semantic search
    embedding_id = Column(String, nullable=True)  # ID in Qdrant

    is_primary = Column(String, default=False)  # Is this the user's primary resume
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="resumes")
    match_scores = relationship("MatchScore", back_populates="resume", cascade="all, delete-orphan")
