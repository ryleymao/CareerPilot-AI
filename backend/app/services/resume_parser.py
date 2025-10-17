"""Resume parser service using pyresparser and custom extraction logic."""
import re
import spacy
from typing import Dict, List, Optional, Any
from pathlib import Path
import PyPDF2
from docx import Document
from pyresparser import ResumeParser


class EnhancedResumeParser:
    """Enhanced resume parser with custom NLP extraction."""

    def __init__(self):
        """Initialize parser with spaCy model."""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            # Model not found, download it
            import subprocess
            subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
            self.nlp = spacy.load("en_core_web_sm")

        # Tech skills database (expandable)
        self.tech_skills = {
            # Programming Languages
            "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go", "rust",
            "php", "swift", "kotlin", "scala", "r", "matlab", "sql",

            # Frameworks & Libraries
            "react", "angular", "vue", "node.js", "express", "fastapi", "django", "flask",
            "spring", "spring boot", "pytorch", "tensorflow", "keras", "scikit-learn",
            "pandas", "numpy", "matplotlib", "seaborn",

            # Databases
            "postgresql", "mysql", "mongodb", "redis", "elasticsearch", "cassandra",
            "dynamodb", "bigquery", "snowflake", "oracle",

            # Cloud & DevOps
            "aws", "azure", "gcp", "docker", "kubernetes", "jenkins", "gitlab", "github actions",
            "terraform", "ansible", "ec2", "s3", "lambda", "rds",

            # Tools & Technologies
            "git", "linux", "bash", "rest api", "graphql", "microservices", "ci/cd",
            "agile", "scrum", "jira", "confluence",
        }

        # Experience level keywords
        self.experience_keywords = {
            "entry": ["entry", "junior", "associate", "graduate", "intern"],
            "mid": ["mid-level", "intermediate", "engineer", "developer", "analyst"],
            "senior": ["senior", "lead", "principal", "staff", "architect", "manager"]
        }

    def extract_text_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF file."""
        text = ""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
        return text

    def extract_text_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX file."""
        text = ""
        try:
            doc = Document(file_path)
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
        return text

    def extract_text(self, file_path: str) -> str:
        """Extract text from resume file."""
        file_path_obj = Path(file_path)
        extension = file_path_obj.suffix.lower()

        if extension == '.pdf':
            return self.extract_text_from_pdf(file_path)
        elif extension in ['.docx', '.doc']:
            return self.extract_text_from_docx(file_path)
        elif extension == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        else:
            raise ValueError(f"Unsupported file format: {extension}")

    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume text."""
        text_lower = text.lower()
        found_skills = set()

        # Extract exact matches
        for skill in self.tech_skills:
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill)

        # Use spaCy NER for additional skill extraction
        doc = self.nlp(text)
        for ent in doc.ents:
            if ent.label_ in ["PRODUCT", "ORG"]:
                skill = ent.text.lower()
                if skill in self.tech_skills:
                    found_skills.add(skill)

        return sorted(list(found_skills))

    def extract_experience_years(self, text: str) -> Optional[int]:
        """Extract years of experience from resume."""
        patterns = [
            r'(\d+)\+?\s*years?\s+(?:of\s+)?experience',
            r'experience\s*:\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s+(?:of\s+)?exp',
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])

        # Fallback: estimate from work history dates
        year_pattern = r'\b(19|20)\d{2}\b'
        years = re.findall(year_pattern, text)
        if len(years) >= 2:
            years_int = [int(y) for y in years]
            earliest = min(years_int)
            latest = max(years_int)
            # Assume work experience spans from earliest to latest year
            from datetime import datetime
            current_year = datetime.now().year
            estimated_years = current_year - earliest
            return min(estimated_years, 50)  # Cap at reasonable max

        return None

    def extract_education(self, text: str) -> List[Dict[str, str]]:
        """Extract education information."""
        education = []

        # Common degree patterns
        degree_patterns = [
            r'\b(bachelor|bs|ba|b\.s\.|b\.a\.)\s+(?:of\s+)?(?:science|arts)?\s*(?:in\s+)?([^\n,]+)',
            r'\b(master|ms|ma|m\.s\.|m\.a\.)\s+(?:of\s+)?(?:science|arts)?\s*(?:in\s+)?([^\n,]+)',
            r'\b(phd|ph\.d\.|doctorate)\s*(?:in\s+)?([^\n,]+)',
            r'\b(associate|as|a\.s\.)\s*(?:in\s+)?([^\n,]+)',
        ]

        for pattern in degree_patterns:
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                degree_type = match.group(1)
                field = match.group(2).strip() if len(match.groups()) > 1 else ""
                education.append({
                    "degree": degree_type,
                    "field": field[:100]  # Truncate if too long
                })

        return education

    def parse_resume(self, file_path: str) -> Dict[str, Any]:
        """
        Parse resume and extract structured information.

        Args:
            file_path: Path to resume file

        Returns:
            Dictionary with parsed resume data
        """
        # Extract raw text
        raw_text = self.extract_text(file_path)

        # Try using pyresparser for basic extraction
        parsed_basic = {}
        try:
            parser = ResumeParser(file_path)
            parsed_basic = parser.get_extracted_data()
        except Exception as e:
            print(f"pyresparser failed: {e}. Using custom extraction only.")

        # Custom extraction
        skills = self.extract_skills(raw_text)
        experience_years = self.extract_experience_years(raw_text)
        education = self.extract_education(raw_text)

        # Use spaCy for name and email extraction if pyresparser failed
        doc = self.nlp(raw_text)

        name = parsed_basic.get("name")
        if not name:
            # Extract first PERSON entity as name
            for ent in doc.ents:
                if ent.label_ == "PERSON":
                    name = ent.text
                    break

        email = parsed_basic.get("email")
        if not email:
            # Extract email with regex
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, raw_text)
            email = emails[0] if emails else None

        phone = parsed_basic.get("mobile_number")
        if not phone:
            # Extract phone number
            phone_pattern = r'(\+?\d{1,3}[-.]?)?\(?\d{3}\)?[-.]?\d{3}[-.]?\d{4}'
            phones = re.findall(phone_pattern, raw_text)
            phone = phones[0] if phones else None

        # Combine all parsed data
        result = {
            "name": name,
            "email": email,
            "phone": phone,
            "skills": skills,
            "experience_years": experience_years,
            "education": education,
            "raw_text": raw_text,
            "parsed_basic": parsed_basic,  # Include original pyresparser output
        }

        return result


# Singleton instance
resume_parser = EnhancedResumeParser()
