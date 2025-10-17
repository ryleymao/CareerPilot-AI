"""Job scraper using JobSpy library."""
from typing import List, Dict, Optional, Any
from datetime import datetime
import re
from jobspy import scrape_jobs


class JobScraper:
    """Scrape jobs from multiple sources using JobSpy."""

    SUPPORTED_SITES = ["indeed", "linkedin", "zip_recruiter", "glassdoor", "google"]

    def __init__(self):
        """Initialize job scraper."""
        pass

    def extract_skills_from_description(self, description: str) -> List[str]:
        """Extract technical skills from job description."""
        # Common tech skills to look for
        tech_skills = {
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
            "react", "angular", "vue", "node.js", "express", "fastapi", "django", "flask",
            "spring", "pytorch", "tensorflow", "sklearn", "pandas", "numpy",
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch",
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
            "git", "linux", "rest api", "graphql", "microservices",
        }

        description_lower = description.lower()
        found_skills = []

        for skill in tech_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, description_lower):
                found_skills.append(skill)

        return found_skills

    def parse_experience_level(self, description: str, title: str) -> Optional[str]:
        """Determine experience level from job posting."""
        combined_text = (title + " " + description).lower()

        if any(word in combined_text for word in ["senior", "lead", "principal", "staff", "architect"]):
            return "senior"
        elif any(word in combined_text for word in ["junior", "entry", "associate", "graduate"]):
            return "entry"
        else:
            return "mid"

    def scrape(
        self,
        search_term: str,
        location: str = "",
        results_wanted: int = 20,
        hours_old: int = 72,
        country: str = "USA",
        sites: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Scrape jobs from multiple job boards.

        Args:
            search_term: Job title or keywords to search
            location: Location to search (city, state, or remote)
            results_wanted: Number of results to return
            hours_old: Only return jobs posted within this many hours
            country: Country to search in
            sites: List of sites to scrape (default: all supported sites)

        Returns:
            List of job dictionaries
        """
        if sites is None:
            sites = ["indeed", "linkedin"]  # Default to most reliable sources

        try:
            # Use JobSpy to scrape jobs
            jobs_df = scrape_jobs(
                site_name=sites,
                search_term=search_term,
                location=location,
                results_wanted=results_wanted,
                hours_old=hours_old,
                country_indeed=country
            )

            # Convert DataFrame to list of dicts
            if jobs_df is None or jobs_df.empty:
                return []

            jobs = []
            for _, row in jobs_df.iterrows():
                # Parse and structure the job data
                description = str(row.get("description", ""))
                title = str(row.get("title", ""))

                # Extract additional information
                required_skills = self.extract_skills_from_description(description)
                experience_level = self.parse_experience_level(description, title)

                job_data = {
                    "title": title,
                    "company": str(row.get("company", "")),
                    "location": str(row.get("location", "")),
                    "job_url": str(row.get("job_url", "")),
                    "description": description,
                    "source": str(row.get("site", "")),
                    "external_id": self.generate_external_id(
                        str(row.get("site", "")),
                        str(row.get("job_url", ""))
                    ),
                    "job_type": str(row.get("job_type", "")),
                    "posted_date": self.parse_date(row.get("date_posted")),
                    "salary_min": self.parse_salary(row.get("min_amount")),
                    "salary_max": self.parse_salary(row.get("max_amount")),
                    "required_skills": required_skills,
                    "experience_level": experience_level,
                    "is_active": True,
                }

                jobs.append(job_data)

            return jobs

        except Exception as e:
            print(f"Error scraping jobs: {e}")
            return []

    def generate_external_id(self, source: str, job_url: str) -> str:
        """Generate unique external ID for a job."""
        # Use hash of source + URL to create unique ID
        import hashlib
        unique_string = f"{source}_{job_url}"
        return hashlib.md5(unique_string.encode()).hexdigest()

    def parse_date(self, date_value: Any) -> Optional[datetime]:
        """Parse date from various formats."""
        if date_value is None:
            return None

        if isinstance(date_value, datetime):
            return date_value

        if isinstance(date_value, str):
            try:
                # Try parsing common date formats
                from dateutil import parser
                return parser.parse(date_value)
            except Exception:
                return None

        return None

    def parse_salary(self, salary_value: Any) -> Optional[float]:
        """Parse salary value."""
        if salary_value is None:
            return None

        try:
            return float(salary_value)
        except (ValueError, TypeError):
            return None

    def scrape_by_preferences(
        self,
        job_titles: List[str],
        locations: List[str],
        results_per_query: int = 20
    ) -> List[Dict[str, Any]]:
        """
        Scrape jobs based on user preferences.

        Args:
            job_titles: List of job titles to search
            locations: List of locations to search
            results_per_query: Results to fetch per query

        Returns:
            Deduplicated list of jobs
        """
        all_jobs = []
        seen_external_ids = set()

        for title in job_titles:
            for location in locations:
                jobs = self.scrape(
                    search_term=title,
                    location=location,
                    results_wanted=results_per_query
                )

                # Deduplicate
                for job in jobs:
                    external_id = job.get("external_id")
                    if external_id and external_id not in seen_external_ids:
                        seen_external_ids.add(external_id)
                        all_jobs.append(job)

        return all_jobs


# Singleton instance
job_scraper = JobScraper()
