"""Resume tailoring service using LLMs."""
from typing import Dict, List, Any, Optional
import requests
from app.config import settings

# Optional imports for cloud APIs
try:
    from anthropic import Anthropic
except ImportError:
    Anthropic = None

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


class ResumeTailorService:
    """Generate resume tailoring suggestions using LLMs."""

    def __init__(self):
        """Initialize tailoring service."""
        self.anthropic_client = None
        self.openai_client = None
        self.llm_provider = settings.LLM_PROVIDER  # "ollama", "anthropic", or "openai"
        self.ollama_model = settings.OLLAMA_MODEL  # Easy to change model!

        # Initialize cloud API clients if available
        if Anthropic and settings.ANTHROPIC_API_KEY:
            self.anthropic_client = Anthropic(api_key=settings.ANTHROPIC_API_KEY)

        if OpenAI and settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama (local LLM) - FREE and UNLIMITED!"""
        try:
            response = requests.post(
                f"{settings.OLLAMA_URL}/api/generate",
                json={
                    "model": self.ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 2000,
                    }
                },
                timeout=60
            )
            response.raise_for_status()
            return response.json()["response"]
        except Exception as e:
            print(f"Ollama error: {e}")
            raise ValueError(f"Ollama not available. Make sure it's running: brew services start ollama")

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic Claude API."""
        if not self.anthropic_client:
            raise ValueError("Anthropic not available. Install: pip install anthropic")

        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI GPT API."""
        if not self.openai_client:
            raise ValueError("OpenAI not available. Install: pip install openai")

        response = self.openai_client.chat.completions.create(
            model="gpt-4-turbo-preview",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content

    def _call_llm(self, prompt: str) -> str:
        """
        Call LLM based on configured provider.

        Priority:
        1. Use configured LLM_PROVIDER
        2. Fallback to Ollama (free & unlimited)
        3. Try Anthropic if available
        4. Try OpenAI if available
        """
        # Use explicitly configured provider
        if self.llm_provider == "ollama":
            return self._call_ollama(prompt)
        elif self.llm_provider == "anthropic" and self.anthropic_client:
            return self._call_anthropic(prompt)
        elif self.llm_provider == "openai" and self.openai_client:
            return self._call_openai(prompt)

        # Fallback logic
        try:
            return self._call_ollama(prompt)
        except Exception:
            if self.anthropic_client:
                return self._call_anthropic(prompt)
            elif self.openai_client:
                return self._call_openai(prompt)
            else:
                raise ValueError(
                    "No LLM available. Either:\n"
                    "1. Start Ollama: brew services start ollama\n"
                    "2. Set ANTHROPIC_API_KEY in .env\n"
                    "3. Set OPENAI_API_KEY in .env"
                )

    def generate_tailoring_suggestions(
        self,
        resume_text: str,
        job_description: str,
        missing_skills: List[str],
        matched_skills: List[str]
    ) -> Dict[str, Any]:
        """
        Generate specific suggestions to tailor resume for a job.

        Args:
            resume_text: Original resume text
            job_description: Target job description
            missing_skills: Skills required by job but not in resume
            matched_skills: Skills that match

        Returns:
            Dictionary with tailoring suggestions
        """
        prompt = f"""You are a professional resume consultant. Analyze the following resume and job description, then provide specific, actionable suggestions to tailor the resume for this job.

RESUME:
{resume_text[:3000]}

JOB DESCRIPTION:
{job_description[:2000]}

MATCHED SKILLS: {', '.join(matched_skills) if matched_skills else 'None identified'}
MISSING SKILLS: {', '.join(missing_skills) if missing_skills else 'None identified'}

Please provide:
1. **Keyword Optimization**: Specific keywords from the job description that should be added to the resume (where truthful and applicable)
2. **Bullet Point Rewrites**: Suggest 3-5 specific bullet points from the resume that could be rewritten to better align with the job description. Provide the original and suggested revision.
3. **Skills to Highlight**: Which existing skills/experiences should be emphasized more prominently
4. **Overall Strategy**: Brief advice on positioning and framing

IMPORTANT: Only suggest changes that are truthful and based on existing experience. Do not fabricate qualifications.

Format your response as JSON with keys: keyword_suggestions, bullet_rewrites, skills_to_highlight, overall_strategy"""

        try:
            response = self._call_llm(prompt)

            # Parse response (attempt JSON, fallback to structured text)
            import json
            try:
                suggestions = json.loads(response)
            except json.JSONDecodeError:
                # Fallback: parse as structured text
                suggestions = {
                    "keyword_suggestions": [],
                    "bullet_rewrites": [],
                    "skills_to_highlight": [],
                    "overall_strategy": response
                }

            return suggestions

        except Exception as e:
            print(f"Error generating tailoring suggestions: {e}")
            return self._generate_fallback_suggestions(missing_skills, matched_skills)

    def _generate_fallback_suggestions(
        self,
        missing_skills: List[str],
        matched_skills: List[str]
    ) -> Dict[str, Any]:
        """Generate basic suggestions without LLM."""
        keyword_suggestions = missing_skills[:10] if missing_skills else []

        return {
            "keyword_suggestions": keyword_suggestions,
            "bullet_rewrites": [
                {
                    "suggestion": f"Add mentions of: {', '.join(keyword_suggestions[:5])}"
                }
            ],
            "skills_to_highlight": matched_skills[:5],
            "overall_strategy": "Emphasize matched skills and consider adding missing skills where applicable."
        }

    def rewrite_bullet_point(
        self,
        original_bullet: str,
        job_keywords: List[str]
    ) -> str:
        """
        Rewrite a single bullet point to include job keywords.

        Args:
            original_bullet: Original bullet point text
            job_keywords: Keywords to incorporate

        Returns:
            Rewritten bullet point
        """
        prompt = f"""Rewrite the following resume bullet point to naturally incorporate these keywords: {', '.join(job_keywords)}

Original: {original_bullet}

Rewritten bullet point (keep it truthful, concise, and natural):"""

        try:
            return self._call_llm(prompt).strip()
        except Exception as e:
            print(f"Error rewriting bullet: {e}")
            return original_bullet

    def generate_tailored_resume(
        self,
        resume_text: str,
        job_description: str,
        suggestions: Dict[str, Any]
    ) -> str:
        """
        Generate a full tailored resume based on suggestions.

        Args:
            resume_text: Original resume
            job_description: Target job description
            suggestions: Tailoring suggestions

        Returns:
            Tailored resume text
        """
        prompt = f"""You are an expert resume writer. Create a tailored version of this resume optimized for the job description below.

ORIGINAL RESUME:
{resume_text}

TARGET JOB:
{job_description[:1500]}

TAILORING SUGGESTIONS:
{suggestions}

Please generate an optimized version of the resume that:
1. Incorporates relevant keywords naturally
2. Emphasizes relevant experience and skills
3. Maintains 100% truthfulness (do not fabricate)
4. Keeps professional formatting
5. Stays approximately the same length

Return ONLY the tailored resume text, ready to use."""

        try:
            tailored_resume = self._call_llm(prompt)
            return tailored_resume
        except Exception as e:
            print(f"Error generating tailored resume: {e}")
            # Fallback: return original with note
            return resume_text + "\n\n[Note: Auto-tailoring unavailable. Please manually incorporate suggested keywords.]"

    def generate_cover_letter(
        self,
        resume_text: str,
        job_description: str,
        company_name: str,
        job_title: str
    ) -> str:
        """
        Generate a cover letter for the job application.

        Args:
            resume_text: Applicant's resume
            job_description: Job description
            company_name: Company name
            job_title: Job title

        Returns:
            Generated cover letter
        """
        prompt = f"""Write a compelling cover letter for this job application:

APPLICANT'S RESUME:
{resume_text[:2000]}

JOB TITLE: {job_title}
COMPANY: {company_name}

JOB DESCRIPTION:
{job_description[:1500]}

Write a professional, personalized cover letter that:
1. Shows enthusiasm for the role and company
2. Highlights relevant experience and skills from the resume
3. Demonstrates understanding of the job requirements
4. Is concise (3-4 paragraphs, ~300 words)
5. Includes proper formatting with [Your Name], [Your Email], and [Date] placeholders

Return only the cover letter text."""

        try:
            cover_letter = self._call_llm(prompt)
            return cover_letter
        except Exception as e:
            print(f"Error generating cover letter: {e}")
            return f"""[Your Name]
[Your Email]
[Date]

Hiring Manager
{company_name}

Dear Hiring Manager,

I am writing to express my strong interest in the {job_title} position at {company_name}.

[Auto-generation unavailable. Please write your cover letter manually.]

Thank you for your consideration.

Sincerely,
[Your Name]"""


# Singleton instance
resume_tailor_service = ResumeTailorService()
