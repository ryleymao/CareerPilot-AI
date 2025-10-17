"""Celery application for background tasks."""
from celery import Celery
from app.config import settings

celery_app = Celery(
    "jobright",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)


@celery_app.task
def scrape_jobs_task(search_term: str, location: str = "", results_wanted: int = 20):
    """Background task to scrape jobs."""
    from app.scrapers.job_scraper import job_scraper
    from app.database import SessionLocal
    from app.models.job import Job
    from app.ml.embeddings import embedding_service

    db = SessionLocal()
    try:
        jobs_data = job_scraper.scrape(
            search_term=search_term,
            location=location,
            results_wanted=results_wanted
        )

        for job_data in jobs_data:
            existing = db.query(Job).filter(
                Job.external_id == job_data["external_id"]
            ).first()

            if not existing:
                job = Job(**job_data)
                db.add(job)
                db.flush()

                # Generate embedding
                try:
                    embedding_id = embedding_service.store_job_embedding(
                        job_id=job.id,
                        text=job.description,
                        metadata={"title": job.title, "company": job.company}
                    )
                    job.embedding_id = embedding_id
                except Exception as e:
                    print(f"Error generating embedding: {e}")

        db.commit()
        return {"status": "success", "jobs_scraped": len(jobs_data)}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@celery_app.task
def calculate_match_task(resume_id: int, job_id: int):
    """Background task to calculate match score."""
    from app.ml.matching import matching_engine
    from app.database import SessionLocal
    from app.models.resume import Resume
    from app.models.job import Job
    from app.models.match_score import MatchScore

    db = SessionLocal()
    try:
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        job = db.query(Job).filter(Job.id == job_id).first()

        if not resume or not job:
            return {"status": "error", "message": "Resume or job not found"}

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
            "location": job.location or "",
        }

        match_result = matching_engine.match_resume_to_job(resume_data, job_data)

        # Store result
        existing_match = db.query(MatchScore).filter(
            MatchScore.resume_id == resume_id,
            MatchScore.job_id == job_id
        ).first()

        if existing_match:
            for key, value in match_result.items():
                setattr(existing_match, key, value)
        else:
            match_score = MatchScore(resume_id=resume_id, job_id=job_id, **match_result)
            db.add(match_score)

        db.commit()
        return {"status": "success", "score": match_result["overall_score"]}

    except Exception as e:
        db.rollback()
        return {"status": "error", "message": str(e)}
    finally:
        db.close()
