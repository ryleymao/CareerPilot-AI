"""Job management endpoints."""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel

from app.database import get_db
from app.models.job import Job
from app.scrapers.job_scraper import job_scraper
from app.ml.embeddings import embedding_service
from app.services.ai_job_discovery import AIJobDiscovery

router = APIRouter()


class JobSearchRequest(BaseModel):
    """Job search request model."""
    search_term: str
    location: str = ""
    results_wanted: int = 20


@router.post("/discover")
async def discover_jobs_ai(
    request: JobSearchRequest,
    db: Session = Depends(get_db)
):
    """
    🤖 AI-POWERED Job Discovery (Recommended!)

    Unlike basic scrapers, this uses AI to find ONLY:
    - Fresh jobs (posted in last 14 days, not 90!)
    - Legitimate postings (no spam/scams)
    - High-quality jobs (quality score > 70%)
    - Deduplicated results

    Example:
    {
        "search_term": "Software Engineer",
        "location": "Remote",
        "results_wanted": 50
    }
    """
    try:
        discovery = AIJobDiscovery(db)

        jobs = discovery.discover_jobs(
            search_term=request.search_term,
            location=request.location,
            max_results=request.results_wanted,
            max_age_days=14  # Only last 2 weeks
        )

        # Save to database
        added_count = 0
        for job_data in jobs:
            discovery._save_job_to_db(job_data)
            added_count += 1

        return {
            "message": "AI job discovery completed",
            "jobs_found": len(jobs),
            "added_to_database": added_count,
            "quality_filter": "Only fresh, legitimate, high-quality jobs"
        }

    except Exception as e:
        raise HTTPException(500, f"AI discovery error: {str(e)}")


@router.post("/scrape")
async def scrape_jobs(
    request: JobSearchRequest,
    db: Session = Depends(get_db)
):
    """
    Basic job scraping (fallback method).

    ⚠️ May include old/spam jobs. Use /discover for AI-powered search instead!

    Example:
    {
        "search_term": "Python Developer",
        "location": "San Francisco, CA",
        "results_wanted": 50
    }
    """
    try:
        # Scrape jobs
        jobs_data = job_scraper.scrape(
            search_term=request.search_term,
            location=request.location,
            results_wanted=request.results_wanted
        )

        added_count = 0
        updated_count = 0

        for job_data in jobs_data:
            # Check if job already exists
            existing = db.query(Job).filter(
                Job.external_id == job_data["external_id"]
            ).first()

            if existing:
                # Update existing job
                for key, value in job_data.items():
                    setattr(existing, key, value)
                updated_count += 1
            else:
                # Create new job
                job = Job(**job_data)
                db.add(job)
                added_count += 1

        db.commit()

        # Generate embeddings for new jobs (async in production)
        new_jobs = db.query(Job).filter(Job.embedding_id == None).limit(100).all()
        for job in new_jobs:
            try:
                embedding_id = embedding_service.store_job_embedding(
                    job_id=job.id,
                    text=job.description,
                    metadata={
                        "title": job.title,
                        "company": job.company,
                        "location": job.location
                    }
                )
                job.embedding_id = embedding_id
                db.commit()
            except Exception as e:
                print(f"Error generating embedding for job {job.id}: {e}")

        return {
            "message": "Jobs scraped successfully",
            "added": added_count,
            "updated": updated_count,
            "total": len(jobs_data)
        }

    except Exception as e:
        db.rollback()
        raise HTTPException(500, f"Error scraping jobs: {str(e)}")


@router.get("/")
async def list_jobs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """List jobs with pagination and optional search."""
    query = db.query(Job).filter(Job.is_active == True)

    if search:
        query = query.filter(
            (Job.title.ilike(f"%{search}%")) |
            (Job.company.ilike(f"%{search}%"))
        )

    total = query.count()
    jobs = query.offset(skip).limit(limit).all()

    return {
        "total": total,
        "jobs": [
            {
                "id": job.id,
                "title": job.title,
                "company": job.company,
                "location": job.location,
                "job_type": job.job_type,
                "experience_level": job.experience_level,
                "posted_date": job.posted_date,
                "job_url": job.job_url,
                "source": job.source,
            }
            for job in jobs
        ]
    }


@router.get("/{job_id}")
async def get_job(job_id: int, db: Session = Depends(get_db)):
    """Get detailed job information."""
    job = db.query(Job).filter(Job.id == job_id).first()

    if not job:
        raise HTTPException(404, "Job not found")

    return {
        "id": job.id,
        "title": job.title,
        "company": job.company,
        "location": job.location,
        "description": job.description,
        "requirements": job.requirements,
        "job_type": job.job_type,
        "experience_level": job.experience_level,
        "required_skills": job.required_skills,
        "nice_to_have_skills": job.nice_to_have_skills,
        "salary_min": job.salary_min,
        "salary_max": job.salary_max,
        "job_url": job.job_url,
        "source": job.source,
        "posted_date": job.posted_date,
    }
