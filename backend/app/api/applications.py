"""Application tracking endpoints."""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional

from app.database import get_db
from app.models.application import Application
from app.models.job import Job

router = APIRouter()


class ApplicationCreate(BaseModel):
    """Application creation model."""
    job_id: int
    resume_id: int
    tailored_resume: Optional[str] = None
    cover_letter: Optional[str] = None
    notes: Optional[str] = None


@router.post("/")
async def create_application(
    application: ApplicationCreate,
    db: Session = Depends(get_db)
):
    """Create a new job application record."""
    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job:
        raise HTTPException(404, "Job not found")

    app = Application(
        user_id=1,  # TODO: Get from auth
        job_id=application.job_id,
        status="pending",
        tailored_resume=application.tailored_resume,
        cover_letter=application.cover_letter,
        notes=application.notes,
        auto_applied=False
    )

    db.add(app)
    db.commit()
    db.refresh(app)

    return {
        "application_id": app.id,
        "job_id": app.job_id,
        "status": app.status,
        "applied_at": app.applied_at,
        "message": "Application created successfully"
    }


@router.get("/")
async def list_applications(db: Session = Depends(get_db)):
    """List all applications for user."""
    # TODO: Filter by authenticated user
    applications = db.query(Application).all()

    results = []
    for app in applications:
        job = db.query(Job).filter(Job.id == app.job_id).first()
        results.append({
            "application_id": app.id,
            "job_id": app.job_id,
            "job_title": job.title if job else "N/A",
            "company": job.company if job else "N/A",
            "status": app.status,
            "applied_at": app.applied_at,
            "auto_applied": app.auto_applied,
            "notes": app.notes
        })

    return {"applications": results, "total": len(results)}


@router.get("/{application_id}")
async def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get detailed application information."""
    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(404, "Application not found")

    job = db.query(Job).filter(Job.id == app.job_id).first()

    return {
        "application_id": app.id,
        "job_id": app.job_id,
        "job_title": job.title if job else "N/A",
        "company": job.company if job else "N/A",
        "job_url": job.job_url if job else None,
        "status": app.status,
        "applied_at": app.applied_at,
        "tailored_resume": app.tailored_resume,
        "cover_letter": app.cover_letter,
        "notes": app.notes,
        "auto_applied": app.auto_applied
    }


@router.patch("/{application_id}/status")
async def update_application_status(
    application_id: int,
    status: str,
    db: Session = Depends(get_db)
):
    """Update application status."""
    valid_statuses = ["pending", "submitted", "rejected", "interview", "offer"]
    if status not in valid_statuses:
        raise HTTPException(400, f"Invalid status. Must be one of: {valid_statuses}")

    app = db.query(Application).filter(Application.id == application_id).first()
    if not app:
        raise HTTPException(404, "Application not found")

    app.status = status
    db.commit()

    return {"application_id": app.id, "status": app.status}
