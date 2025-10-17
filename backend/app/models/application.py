"""Application model."""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Application(Base):
    """Job application model."""

    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    job_id = Column(Integer, ForeignKey("jobs.id"), nullable=False)

    # Application status
    status = Column(String, default="pending")  # pending, submitted, rejected, interview, offer
    applied_at = Column(DateTime(timezone=True), server_default=func.now())

    # Tailored resume used for this application
    tailored_resume = Column(Text, nullable=True)
    cover_letter = Column(Text, nullable=True)

    # Auto-apply details
    auto_applied = Column(String, default=False)
    application_data = Column(JSON, nullable=True)  # Form data submitted
    screenshot_path = Column(String, nullable=True)  # Screenshot of confirmation

    # Notes and tracking
    notes = Column(Text, nullable=True)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="applications")
    job = relationship("Job", back_populates="applications")
