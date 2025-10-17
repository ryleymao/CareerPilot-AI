"""Resume-Job matching engine."""
from typing import Dict, List, Any, Tuple
from app.ml.embeddings import embedding_service


class MatchingEngine:
    """Match resumes to jobs with detailed scoring."""

    # Scoring weights
    WEIGHTS = {
        "keyword": 0.30,
        "semantic": 0.40,
        "experience": 0.15,
        "education": 0.10,
        "location": 0.05,
    }

    def calculate_keyword_score(
        self,
        resume_skills: List[str],
        job_skills: List[str]
    ) -> Tuple[float, List[str], List[str]]:
        """
        Calculate keyword overlap score.

        Args:
            resume_skills: Skills from resume
            job_skills: Required skills from job

        Returns:
            (score, matched_skills, missing_skills)
        """
        if not job_skills:
            return 1.0, [], []

        resume_skills_lower = [s.lower() for s in resume_skills]
        job_skills_lower = [s.lower() for s in job_skills]

        matched = []
        missing = []

        for skill in job_skills_lower:
            if skill in resume_skills_lower:
                matched.append(skill)
            else:
                missing.append(skill)

        score = len(matched) / len(job_skills_lower) if job_skills_lower else 0
        return score, matched, missing

    def calculate_semantic_score(
        self,
        resume_text: str,
        job_description: str
    ) -> float:
        """
        Calculate semantic similarity score.

        Args:
            resume_text: Resume full text
            job_description: Job description full text

        Returns:
            Semantic similarity score (0-1)
        """
        return embedding_service.compute_similarity(resume_text, job_description)

    def calculate_experience_score(
        self,
        resume_years: int,
        job_level: str
    ) -> float:
        """
        Calculate experience match score.

        Args:
            resume_years: Years of experience in resume
            job_level: Job experience level (entry, mid, senior)

        Returns:
            Experience match score (0-1)
        """
        if resume_years is None:
            return 0.5  # Neutral if unknown

        # Expected years for each level
        level_ranges = {
            "entry": (0, 2),
            "mid": (2, 5),
            "senior": (5, 100),
        }

        if job_level not in level_ranges:
            return 0.5

        min_years, max_years = level_ranges[job_level]

        if min_years <= resume_years <= max_years:
            return 1.0
        elif resume_years < min_years:
            # Under-qualified, but not zero
            gap = min_years - resume_years
            return max(0.3, 1.0 - (gap * 0.2))
        else:
            # Over-qualified
            excess = resume_years - max_years
            return max(0.7, 1.0 - (excess * 0.05))

    def calculate_education_score(
        self,
        resume_education: List[Dict[str, str]],
        job_description: str
    ) -> float:
        """
        Calculate education match score.

        Args:
            resume_education: List of education entries
            job_description: Job description to check requirements

        Returns:
            Education match score (0-1)
        """
        if not resume_education:
            # Check if job requires degree
            job_desc_lower = job_description.lower()
            requires_degree = any(word in job_desc_lower for word in ["bachelor", "master", "phd", "degree required"])

            if requires_degree:
                return 0.3  # Penalty if degree required but not found
            else:
                return 0.8  # Neutral if not required

        # Has some education
        degrees = [edu.get("degree", "").lower() for edu in resume_education]

        if any("phd" in d or "doctorate" in d for d in degrees):
            return 1.0
        elif any("master" in d or "ms" in d or "ma" in d for d in degrees):
            return 0.9
        elif any("bachelor" in d or "bs" in d or "ba" in d for d in degrees):
            return 0.8
        else:
            return 0.6

    def calculate_location_score(
        self,
        resume_location: str,
        job_location: str
    ) -> float:
        """
        Calculate location match bonus.

        Args:
            resume_location: Resume location (if available)
            job_location: Job location

        Returns:
            Location bonus (0-1)
        """
        if not job_location:
            return 1.0

        job_loc_lower = job_location.lower()

        # Remote jobs get full score
        if "remote" in job_loc_lower:
            return 1.0

        # If no resume location, neutral score
        if not resume_location:
            return 0.5

        resume_loc_lower = resume_location.lower()

        # Check for match
        if resume_loc_lower in job_loc_lower or job_loc_lower in resume_loc_lower:
            return 1.0

        return 0.3  # Different location penalty

    def analyze_strengths_and_gaps(
        self,
        resume_data: Dict[str, Any],
        job_data: Dict[str, Any],
        matched_skills: List[str],
        missing_skills: List[str],
        scores: Dict[str, float]
    ) -> Tuple[List[str], List[str]]:
        """
        Analyze strengths and gaps.

        Returns:
            (strengths, gaps)
        """
        strengths = []
        gaps = []

        # Skills strengths/gaps
        if matched_skills:
            strengths.append(f"Strong match on {len(matched_skills)} key skills: {', '.join(matched_skills[:5])}")

        if missing_skills:
            gaps.append(f"Missing {len(missing_skills)} required skills: {', '.join(missing_skills[:5])}")

        # Experience
        exp_score = scores.get("experience", 0)
        if exp_score >= 0.8:
            strengths.append("Experience level matches job requirements")
        elif exp_score < 0.5:
            gaps.append("Experience level may not match job requirements")

        # Education
        edu_score = scores.get("education", 0)
        if edu_score >= 0.8:
            strengths.append("Educational background aligns well")
        elif edu_score < 0.5:
            gaps.append("Educational requirements may not be fully met")

        return strengths, gaps

    def match_resume_to_job(
        self,
        resume_data: Dict[str, Any],
        job_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Calculate comprehensive match score between resume and job.

        Args:
            resume_data: Parsed resume data with keys:
                - raw_text, skills, experience_years, education, etc.
            job_data: Job data with keys:
                - description, required_skills, experience_level, location, etc.

        Returns:
            Dictionary with match results
        """
        # Extract data
        resume_text = resume_data.get("raw_text", "")
        resume_skills = resume_data.get("skills", [])
        resume_years = resume_data.get("experience_years")
        resume_education = resume_data.get("education", [])
        resume_location = resume_data.get("location", "")

        job_description = job_data.get("description", "")
        job_skills = job_data.get("required_skills", [])
        job_level = job_data.get("experience_level", "mid")
        job_location = job_data.get("location", "")

        # Calculate sub-scores
        keyword_score, matched_skills, missing_skills = self.calculate_keyword_score(
            resume_skills, job_skills
        )

        semantic_score = self.calculate_semantic_score(resume_text, job_description)
        experience_score = self.calculate_experience_score(resume_years, job_level)
        education_score = self.calculate_education_score(resume_education, job_description)
        location_score = self.calculate_location_score(resume_location, job_location)

        # Weighted overall score
        overall_score = (
            self.WEIGHTS["keyword"] * keyword_score +
            self.WEIGHTS["semantic"] * semantic_score +
            self.WEIGHTS["experience"] * experience_score +
            self.WEIGHTS["education"] * education_score +
            self.WEIGHTS["location"] * location_score
        )

        # Convert to 0-100 scale
        overall_score_pct = round(overall_score * 100, 1)

        # Store sub-scores
        scores = {
            "keyword": keyword_score,
            "semantic": semantic_score,
            "experience": experience_score,
            "education": education_score,
            "location": location_score,
        }

        # Analyze strengths and gaps
        strengths, gaps = self.analyze_strengths_and_gaps(
            resume_data, job_data, matched_skills, missing_skills, scores
        )

        return {
            "overall_score": overall_score_pct,
            "keyword_score": round(keyword_score * 100, 1),
            "semantic_score": round(semantic_score * 100, 1),
            "experience_score": round(experience_score * 100, 1),
            "education_score": round(education_score * 100, 1),
            "location_score": round(location_score * 100, 1),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "strengths": strengths,
            "gaps": gaps,
        }


# Singleton instance
matching_engine = MatchingEngine()
