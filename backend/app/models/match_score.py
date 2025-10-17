"""Match score model."""
from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class MatchScore(Base):
    """Resume-Job match score model."""

    __tablename__ = "match_scores"

    id = Column(Integer, primary_key=True, index=True)
    resume_id = Column(Integer, ForeignKey("resumes.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    # Overall match score (0-100)
    overall_score = Column(Float, nullable=False, index=True)

    # Sub-scores
    keyword_score = Column(Float, nullable=True)  # Keyword overlap score
    semantic_score = Column(Float, nullable=True)  # Embedding similarity score
    experience_score = Column(Float, nullable=True)  # Experience match score
    education_score = Column(Float, nullable=True)  # Education match score
    location_score = Column(Float, nullable=True)  # Location bonus

    # Detailed breakdown
    matched_skills = Column(JSON, nullable=True)  # List of matched skills
    missing_skills = Column(JSON, nullable=True)  # List of missing skills
    strengths = Column(JSON, nullable=True)  # List of strength points
    gaps = Column(JSON, nullable=True)  # List of gaps/weaknesses

    # Tailoring suggestions
    suggestions = Column(JSON, nullable=True)  # List of improvement suggestions

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    resume = relationship("Resume", back_populates="match_scores")
    job = relationship("Job", back_populates="match_scores")
