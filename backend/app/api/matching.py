"""Job matching endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel

from app.database import get_db
from app.models.resume import Resume
from app.models.job import Job
from app.models.match_score import MatchScore
from app.ml.matching import matching_engine
from app.services.resume_tailor import resume_tailor_service

router = APIRouter()


class TailorRequest(BaseModel):
    """Resume tailoring request."""
    resume_id: int
    job_id: int


@router.post("/calculate/{resume_id}/{job_id}")
async def calculate_match(
    resume_id: int,
    job_id: int,
    db: Session = Depends(get_db)
):
    """
    Calculate match score between a resume and job.

    Returns detailed matching analysis with score breakdown.
    """
    # Get resume and job
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    job = db.query(Job).filter(Job.id == job_id).first()

    if not resume:
        raise HTTPException(404, "Resume not found")
    if not job:
        raise HTTPException(404, "Job not found")

    # Prepare data for matching
    resume_data = {
        "raw_text": resume.raw_text,
        "skills": resume.skills or [],
        "experience_years": resume.experience_years,
        "education": resume.education or [],
        "location": "",  # TODO: Extract from parsed data
    }

    job_data = {
        "description": job.description,
        "required_skills": job.required_skills or [],
        "experience_level": job.experience_level or "mid",
        "location": job.location or "",
    }

    # Calculate match
    match_result = matching_engine.match_resume_to_job(resume_data, job_data)

    # Check if match score already exists
    existing_match = db.query(MatchScore).filter(
        MatchScore.resume_id == resume_id,
        MatchScore.job_id == job_id
    ).first()

    if existing_match:
        # Update existing
        existing_match.overall_score = match_result["overall_score"]
        existing_match.keyword_score = match_result["keyword_score"]
        existing_match.semantic_score = match_result["semantic_score"]
        existing_match.experience_score = match_result["experience_score"]
        existing_match.education_score = match_result["education_score"]
        existing_match.location_score = match_result["location_score"]
        existing_match.matched_skills = match_result["matched_skills"]
        existing_match.missing_skills = match_result["missing_skills"]
        existing_match.strengths = match_result["strengths"]
        existing_match.gaps = match_result["gaps"]
    else:
        # Create new
        match_score = MatchScore(
            resume_id=resume_id,
            job_id=job_id,
            overall_score=match_result["overall_score"],
            keyword_score=match_result["keyword_score"],
            semantic_score=match_result["semantic_score"],
            experience_score=match_result["experience_score"],
            education_score=match_result["education_score"],
            location_score=match_result["location_score"],
            matched_skills=match_result["matched_skills"],
            missing_skills=match_result["missing_skills"],
            strengths=match_result["strengths"],
            gaps=match_result["gaps"],
        )
        db.add(match_score)

    db.commit()

    return {
        "resume_id": resume_id,
        "job_id": job_id,
        "job_title": job.title,
        "company": job.company,
        **match_result
    }


@router.get("/matches/{resume_id}")
async def get_matches_for_resume(
    resume_id: int,
    min_score: float = Query(0, ge=0, le=100),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    Get all job matches for a resume, sorted by match score.

    Optionally filter by minimum score.
    """
    resume = db.query(Resume).filter(Resume.id == resume_id).first()
    if not resume:
        raise HTTPException(404, "Resume not found")

    # Get existing match scores
    matches = db.query(MatchScore).filter(
        MatchScore.resume_id == resume_id,
        MatchScore.overall_score >= min_score
    ).order_by(MatchScore.overall_score.desc()).limit(limit).all()

    results = []
    for match in matches:
        job = db.query(Job).filter(Job.id == match.job_id).first()
        if job:
            results.append({
                "job_id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "job_url": job.job_url,
                "overall_score": match.overall_score,
                "matched_skills": match.matched_skills,
                "missing_skills": match.missing_skills,
                "strengths": match.strengths,
                "gaps": match.gaps,
            })

    return {
        "resume_id": resume_id,
        "matches": results,
        "total": len(results)
    }


@router.post("/tailor")
async def tailor_resume(
    request: TailorRequest,
    db: Session = Depends(get_db)
):
    """
    Generate tailoring suggestions for a resume to match a specific job.

    Returns:
    - Keyword suggestions
    - Bullet point rewrites
    - Overall strategy
    """
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    job = db.query(Job).filter(Job.id == request.job_id).first()

    if not resume:
        raise HTTPException(404, "Resume not found")
    if not job:
        raise HTTPException(404, "Job not found")

    # Get or calculate match score
    match = db.query(MatchScore).filter(
        MatchScore.resume_id == request.resume_id,
        MatchScore.job_id == request.job_id
    ).first()

    if not match:
        # Calculate match first
        resume_data = {
            "raw_text": resume.raw_text,
            "skills": resume.skills or [],
            "experience_years": resume.experience_years,
            "education": resume.education or [],
        }
        job_data = {
            "description": job.description,
            "required_skills": job.required_skills or [],
            "experience_level": job.experience_level or "mid",
        }
        match_result = matching_engine.match_resume_to_job(resume_data, job_data)

        matched_skills = match_result["matched_skills"]
        missing_skills = match_result["missing_skills"]
    else:
        matched_skills = match.matched_skills or []
        missing_skills = match.missing_skills or []

    # Generate tailoring suggestions
    suggestions = resume_tailor_service.generate_tailoring_suggestions(
        resume_text=resume.raw_text,
        job_description=job.description,
        missing_skills=missing_skills,
        matched_skills=matched_skills
    )

    # Store suggestions in match_score
    if match:
        match.suggestions = suggestions
        db.commit()

    return {
        "resume_id": request.resume_id,
        "job_id": request.job_id,
        "job_title": job.title,
        "company": job.company,
        "suggestions": suggestions,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills
    }


@router.post("/generate-tailored-resume")
async def generate_tailored_resume(
    request: TailorRequest,
    db: Session = Depends(get_db)
):
    """Generate a fully tailored resume for a specific job."""
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    job = db.query(Job).filter(Job.id == request.job_id).first()

    if not resume or not job:
        raise HTTPException(404, "Resume or job not found")

    # Get match and suggestions
    match = db.query(MatchScore).filter(
        MatchScore.resume_id == request.resume_id,
        MatchScore.job_id == request.job_id
    ).first()

    suggestions = match.suggestions if match and match.suggestions else {}

    # Generate tailored resume
    tailored_resume = resume_tailor_service.generate_tailored_resume(
        resume_text=resume.raw_text,
        job_description=job.description,
        suggestions=suggestions
    )

    return {
        "resume_id": request.resume_id,
        "job_id": request.job_id,
        "tailored_resume": tailored_resume
    }
