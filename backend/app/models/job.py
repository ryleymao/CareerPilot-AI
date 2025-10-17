"""Job model."""
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Job(Base):
    """Job posting model."""

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    # Basic job info
    title = Column(String, nullable=False, index=True)
    company = Column(String, nullable=False, index=True)
    location = Column(String, nullable=True)
    job_url = Column(String, nullable=False)
    source = Column(String, nullable=False)  # indeed, linkedin, glassdoor, etc.
    external_id = Column(String, unique=True, index=True)  # unique ID from source

    # Job details
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=True)
    salary_min = Column(Float, nullable=True)
    salary_max = Column(Float, nullable=True)
    job_type = Column(String, nullable=True)  # full-time, part-time, contract, etc.
    experience_level = Column(String, nullable=True)  # entry, mid, senior, etc.

    # Parsed data
    required_skills = Column(JSON, nullable=True)  # List of required skills
    nice_to_have_skills = Column(JSON, nullable=True)  # List of nice-to-have skills
    benefits = Column(JSON, nullable=True)
    parsed_data = Column(JSON, nullable=True)  # Full parsed job data

    # Embedding for semantic search
    embedding_id = Column(String, nullable=True)  # ID in Qdrant

    # Metadata
    posted_date = Column(DateTime(timezone=True), nullable=True)
    expires_date = Column(DateTime(timezone=True), nullable=True)
    is_active = Column(String, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    match_scores = relationship("MatchScore", back_populates="job", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
