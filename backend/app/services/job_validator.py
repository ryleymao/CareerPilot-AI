"""Job validation service - detect spam and outdated postings."""
from datetime import datetime, timedelta
from typing import Dict, Any, List
import re


class JobValidator:
    """Validate job postings to filter spam and old listings."""

    # Spam indicators
    SPAM_KEYWORDS = [
        'work from home scam', 'pyramid scheme', 'mlm', 'multi-level marketing',
        'pay to work', 'easy money', 'get rich quick', 'no experience needed make $$$',
        'bitcoin investment', 'forex trading course', 'insurance sales only',
    ]

    # Red flag patterns
    RED_FLAGS = [
        r'\$\d{3,},?\d{3}[+]?\s*(per|a)\s*(week|day)',  # Unrealistic salary
        r'send\s+money',
        r'western union',
        r'wire transfer',
        r'cashier.*check',
    ]

    def __init__(self):
        """Initialize validator."""
        pass

    def validate_job(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a job posting.

        Returns:
            {
                "is_valid": bool,
                "is_spam": bool,
                "is_outdated": bool,
                "confidence_score": 0-100,
                "warnings": [list of warnings],
                "age_days": int
            }
        """
        warnings = []
        is_spam = False
        is_outdated = False

        # Check for spam keywords
        description = (job_data.get('description', '') + ' ' +
                      job_data.get('title', '')).lower()

        for keyword in self.SPAM_KEYWORDS:
            if keyword in description:
                is_spam = True
                warnings.append(f"Spam keyword detected: {keyword}")

        # Check red flag patterns
        for pattern in self.RED_FLAGS:
            if re.search(pattern, description, re.IGNORECASE):
                is_spam = True
                warnings.append(f"Suspicious pattern detected")

        # Check for missing critical info
        if not job_data.get('company') or job_data.get('company', '').lower() in ['n/a', 'none', 'unknown']:
            warnings.append("Missing or invalid company name")

        if not job_data.get('description') or len(job_data.get('description', '')) < 100:
            warnings.append("Job description too short or missing")

        # Check job age
        age_days = self._calculate_job_age(job_data.get('posted_date'))

        if age_days:
            if age_days > 90:
                is_outdated = True
                warnings.append(f"Job posting is {age_days} days old (likely filled)")
            elif age_days > 60:
                warnings.append(f"Job posting is {age_days} days old (may be filled)")

        # Check for duplicate/reposted jobs (same title + company)
        # This would check against database in production

        # Calculate confidence score
        confidence_score = 100
        if is_spam:
            confidence_score -= 50
        if is_outdated:
            confidence_score -= 30
        if len(warnings) > 0:
            confidence_score -= (len(warnings) * 5)

        confidence_score = max(0, min(100, confidence_score))

        # Determine if valid
        is_valid = not is_spam and confidence_score >= 40

        return {
            "is_valid": is_valid,
            "is_spam": is_spam,
            "is_outdated": is_outdated,
            "confidence_score": confidence_score,
            "warnings": warnings,
            "age_days": age_days
        }

    def _calculate_job_age(self, posted_date) -> int:
        """Calculate how many days old a job posting is."""
        if not posted_date:
            return None

        if isinstance(posted_date, str):
            try:
                from dateutil import parser
                posted_date = parser.parse(posted_date)
            except:
                return None

        if isinstance(posted_date, datetime):
            age = datetime.now() - posted_date
            return age.days

        return None

    def filter_spam_jobs(self, jobs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Filter out spam and low-quality jobs.

        Returns:
            List of validated jobs with validation metadata
        """
        validated_jobs = []

        for job in jobs:
            validation = self.validate_job(job)

            # Add validation data to job
            job['validation'] = validation

            # Only include valid jobs
            if validation['is_valid']:
                validated_jobs.append(job)

        return validated_jobs

    def get_freshness_label(self, age_days: int) -> str:
        """Get human-readable freshness label."""
        if age_days is None:
            return "Unknown"
        elif age_days < 7:
            return "🟢 Fresh (< 1 week)"
        elif age_days < 30:
            return "🟡 Recent (< 1 month)"
        elif age_days < 60:
            return "🟠 Older (1-2 months)"
        else:
            return "🔴 Very Old (> 2 months)"


# Singleton
job_validator = JobValidator()
