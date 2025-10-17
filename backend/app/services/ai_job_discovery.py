"""
AI-Powered Job Discovery Service

This service goes BEYOND basic scrapers to find fresh, high-quality jobs.
It uses AI to:
- Validate job postings are recent and legitimate
- Score jobs based on quality and relevance
- Filter out duplicate/spam/outdated posts
- Discover jobs from multiple sources intelligently
"""

import requests
from typing import List, Dict, Any
from datetime import datetime, timedelta
import hashlib
from sqlalchemy.orm import Session

from ..models.job import Job
from ..services.job_validator import JobValidator


class AIJobDiscovery:
    """
    Smart job discovery that finds ONLY fresh, legitimate, high-quality jobs.

    Unlike dumb scrapers (Indeed/LinkedIn showing 90-day-old jobs),
    this uses AI to validate quality and freshness.
    """

    def __init__(self, db: Session):
        self.db = db
        self.validator = JobValidator()

    def discover_jobs(
        self,
        search_term: str,
        location: str = "Remote",
        max_results: int = 50,
        max_age_days: int = 14  # Only jobs posted in last 2 weeks!
    ) -> List[Dict[str, Any]]:
        """
        Discover fresh, high-quality jobs using AI validation.

        Returns only:
        - Jobs posted in last 14 days (not 90!)
        - No spam/scam postings
        - Quality score > 70%
        - Deduplicated
        """

        print(f"🔍 AI Job Discovery: Searching for '{search_term}' in '{location}'")
        print(f"📅 Only finding jobs posted in last {max_age_days} days")

        # Get jobs from multiple sources
        all_jobs = []

        # Source 1: JobSpy (Indeed, LinkedIn, ZipRecruiter, Glassdoor)
        print("📥 Fetching from JobSpy sources...")
        jobspy_jobs = self._fetch_from_jobspy(search_term, location, max_results)
        all_jobs.extend(jobspy_jobs)

        # Source 2: Could add more sources here
        # - Adzuna API (free tier)
        # - The Muse API
        # - GitHub Jobs (for tech)
        # - RemoteOK (for remote jobs)

        print(f"📊 Found {len(all_jobs)} total jobs from all sources")

        # AI Validation & Filtering
        print("🤖 AI validating jobs for quality and freshness...")
        validated_jobs = []

        for job in all_jobs:
            # Validate with AI
            validation = self.validator.validate_job(job)

            # Check if job passes quality filters
            if not validation["is_valid"]:
                print(f"❌ Rejected: {job.get('title')} - {validation['warnings']}")
                continue

            if validation["is_spam"]:
                print(f"🚫 Spam detected: {job.get('title')}")
                continue

            if validation["age_days"] > max_age_days:
                print(f"⏰ Too old ({validation['age_days']} days): {job.get('title')}")
                continue

            if validation["confidence_score"] < 0.7:
                print(f"⚠️ Low quality ({validation['confidence_score']}): {job.get('title')}")
                continue

            # Add validation metadata to job
            job["validation"] = validation
            job["ai_quality_score"] = validation["confidence_score"]
            job["age_days"] = validation["age_days"]

            validated_jobs.append(job)

        print(f"✅ {len(validated_jobs)} high-quality, fresh jobs found!")

        # Deduplicate by job signature
        deduplicated = self._deduplicate_jobs(validated_jobs)
        print(f"🔄 {len(deduplicated)} unique jobs after deduplication")

        # Sort by quality score
        deduplicated.sort(key=lambda j: j.get("ai_quality_score", 0), reverse=True)

        # Return top results
        return deduplicated[:max_results]

    def _fetch_from_jobspy(
        self,
        search_term: str,
        location: str,
        max_results: int
    ) -> List[Dict[str, Any]]:
        """Fetch jobs using JobSpy library."""
        try:
            from python_jobspy import scrape_jobs

            # Scrape from multiple sites
            jobs_df = scrape_jobs(
                site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
                search_term=search_term,
                location=location,
                results_wanted=max_results,
                hours_old=336,  # 14 days = 336 hours
                country_indeed='USA'
            )

            # Convert to list of dicts
            jobs = jobs_df.to_dict('records')

            # Normalize field names
            normalized = []
            for job in jobs:
                normalized.append({
                    "title": job.get("title") or job.get("job_title"),
                    "company": job.get("company") or job.get("company_name"),
                    "location": job.get("location"),
                    "description": job.get("description"),
                    "url": job.get("job_url") or job.get("url"),
                    "posted_date": job.get("date_posted") or job.get("posted_date"),
                    "salary_min": job.get("min_amount"),
                    "salary_max": job.get("max_amount"),
                    "job_type": job.get("job_type"),
                    "source": job.get("site"),
                })

            return normalized

        except Exception as e:
            print(f"❌ JobSpy error: {e}")
            return []

    def _deduplicate_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Remove duplicate job postings using content-based signatures.

        Many sites repost the same job - we detect this by creating a
        "signature" based on title + company + location.
        """
        seen_signatures = set()
        unique_jobs = []

        for job in jobs:
            # Create job signature
            signature = self._create_job_signature(job)

            if signature not in seen_signatures:
                seen_signatures.add(signature)
                unique_jobs.append(job)

        return unique_jobs

    def _create_job_signature(self, job: Dict[str, Any]) -> str:
        """Create a unique signature for a job to detect duplicates."""
        title = (job.get("title") or "").lower().strip()
        company = (job.get("company") or "").lower().strip()
        location = (job.get("location") or "").lower().strip()

        # Normalize
        signature_str = f"{title}|{company}|{location}"

        # Hash it
        return hashlib.md5(signature_str.encode()).hexdigest()

    def get_job_freshness_score(self, posted_date: datetime) -> float:
        """
        Calculate freshness score (0-1) based on how recent the job is.

        - Posted today: 1.0
        - Posted 7 days ago: 0.5
        - Posted 14 days ago: 0.0
        """
        if not posted_date:
            return 0.5  # Unknown age, assume medium

        days_ago = (datetime.utcnow() - posted_date).days

        if days_ago < 0:
            return 1.0  # Posted in the future? Treat as fresh
        elif days_ago <= 7:
            return 1.0 - (days_ago / 14)  # Linear decay over 2 weeks
        elif days_ago <= 14:
            return 0.5 - ((days_ago - 7) / 14)
        else:
            return 0.0  # Too old

    def discover_jobs_continuously(
        self,
        search_term: str,
        location: str = "Remote",
        interval_hours: int = 6
    ):
        """
        Continuously discover new jobs every X hours.

        This can be run as a background task to keep finding fresh jobs.
        Use Celery Beat to schedule this.
        """
        while True:
            print(f"🔄 Discovering new jobs for: {search_term}")

            jobs = self.discover_jobs(search_term, location)

            # Save to database
            for job_data in jobs:
                self._save_job_to_db(job_data)

            print(f"💾 Saved {len(jobs)} new jobs to database")
            print(f"⏰ Next discovery in {interval_hours} hours...")

            # Wait for next run
            import time
            time.sleep(interval_hours * 3600)

    def _save_job_to_db(self, job_data: Dict[str, Any]):
        """Save discovered job to database."""
        try:
            # Check if already exists
            signature = self._create_job_signature(job_data)

            existing = self.db.query(Job).filter(
                Job.title == job_data.get("title"),
                Job.company == job_data.get("company")
            ).first()

            if existing:
                return  # Already have this job

            # Create new job
            job = Job(
                title=job_data.get("title"),
                company=job_data.get("company"),
                location=job_data.get("location"),
                description=job_data.get("description"),
                url=job_data.get("url"),
                posted_date=job_data.get("posted_date"),
                salary_min=job_data.get("salary_min"),
                salary_max=job_data.get("salary_max"),
                job_type=job_data.get("job_type"),
                source=job_data.get("source"),
            )

            self.db.add(job)
            self.db.commit()

        except Exception as e:
            print(f"❌ Failed to save job: {e}")
            self.db.rollback()
