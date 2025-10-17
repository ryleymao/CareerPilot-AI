"""Resume management endpoints."""
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from pathlib import Path
import shutil
from typing import List

from app.database import get_db
from app.models.resume import Resume
from app.services.resume_parser import resume_parser
from app.ml.embeddings import embedding_service
from app.config import settings

router = APIRouter()


@router.post("/upload")
async def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and parse resume.

    Returns parsed resume data with skills, experience, etc.
    """
    # Validate file type
    allowed_extensions = [".pdf", ".docx", ".doc", ".txt"]
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(400, f"Unsupported file type. Allowed: {allowed_extensions}")

    # Save file
    upload_dir = Path(settings.UPLOAD_DIR)
    upload_dir.mkdir(exist_ok=True)

    file_path = upload_dir / file.filename
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        # Parse resume
        parsed_data = resume_parser.parse_resume(str(file_path))

        # Create resume record (using user_id=1 for demo)
        resume = Resume(
            user_id=1,  # TODO: Get from auth
            filename=file.filename,
            file_path=str(file_path),
            raw_text=parsed_data["raw_text"],
            parsed_data=parsed_data,
            skills=parsed_data.get("skills", []),
            experience_years=parsed_data.get("experience_years"),
            education=parsed_data.get("education", []),
        )

        db.add(resume)
        db.commit()
        db.refresh(resume)

        # Generate and store embedding
        embedding_id = embedding_service.store_resume_embedding(
            resume_id=resume.id,
            text=parsed_data["raw_text"],
            metadata={"filename": file.filename}
        )

        resume.embedding_id = embedding_id
        db.commit()

        return {
            "resume_id": resume.id,
            "filename": file.filename,
            "parsed_data": parsed_data,
            "message": "Resume uploaded and parsed successfully"
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error processing resume: {str(e)}")


@router.get("/{resume_id}")
async def get_resume(resume_id: int, db: Session = Depends(get_db)):
    """Get resume by ID."""
    resume = db.query(Resume).filter(Resume.id == resume_id).first()

    if not resume:
        raise HTTPException(404, "Resume not found")

    return {
        "id": resume.id,
        "filename": resume.filename,
        "skills": resume.skills,
        "experience_years": resume.experience_years,
        "education": resume.education,
        "parsed_data": resume.parsed_data,
        "created_at": resume.created_at
    }


@router.get("/")
async def list_resumes(db: Session = Depends(get_db)):
    """List all resumes for user."""
    # TODO: Filter by authenticated user
    resumes = db.query(Resume).all()

    return [
        {
            "id": r.id,
            "filename": r.filename,
            "skills": r.skills,
            "experience_years": r.experience_years,
            "created_at": r.created_at
        }
        for r in resumes
    ]
