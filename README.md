# CareerPilot - Your AI-Powered Job Search Copilot

An open-source job search platform that helps you find and apply to jobs using AI-powered resume matching, tailoring, and automation. Like having a personal career assistant!

## Features

- **Resume Upload & Parsing**: Upload PDF/DOCX resumes with intelligent parsing using spaCy NLP
- **Job Scraping**: Automated job scraping from Indeed, LinkedIn, Glassdoor, ZipRecruiter using JobSpy
- **AI-Powered Matching**: Semantic similarity matching using Sentence Transformers (all-MiniLM-L6-v2)
- **Match Scoring**: Comprehensive scoring algorithm with keyword overlap, semantic similarity, experience, education, and location matching
- **Resume Tailoring**: AI-powered suggestions to optimize your resume for specific jobs using Claude/GPT
- **Application Tracking**: Track all your applications in one place
- **Dockerized**: Fully containerized with Docker Compose for easy deployment
- **Privacy-First**: Self-hosted, your data stays on your machine

## Tech Stack

### Backend
- **FastAPI** (Python 3.11) - High-performance REST API
- **PostgreSQL** - Relational database for users, resumes, jobs, applications
- **Redis** - Caching and message queue
- **Qdrant** - Vector database for semantic search
- **Celery** - Background task processing

### ML/AI
- **Sentence Transformers** - Generate embeddings for semantic matching
- **spaCy** - NLP for resume parsing
- **Anthropic Claude / OpenAI GPT** - Resume tailoring and suggestions
- **JobSpy** - Multi-source job scraping

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy

## Quick Start

### Prerequisites
- Docker and Docker Compose installed
- 8GB+ RAM recommended
- (Optional) Anthropic or OpenAI API key for resume tailoring

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/careerpilot.git
cd careerpilot
```

2. **Set up environment variables**
```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add your API keys if desired
```

3. **Start all services**
```bash
docker-compose up -d
```

This will start:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Qdrant (port 6333)
- FastAPI Backend (port 8000)
- Celery Workers
- Nginx (port 80)

4. **Access the application**
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

## Usage Guide

### 1. Upload Your Resume

```bash
curl -X POST "http://localhost:8000/api/resumes/upload" \\
  -F "file=@your_resume.pdf"
```

This will:
- Parse your resume and extract skills, experience, education
- Generate embeddings for semantic matching
- Return a resume_id for future use

### 2. Scrape Jobs

```bash
curl -X POST "http://localhost:8000/api/jobs/scrape" \\
  -H "Content-Type: application/json" \\
  -d '{
    "search_term": "Python Developer",
    "location": "San Francisco, CA",
    "results_wanted": 50
  }'
```

This will scrape jobs from multiple sources and store them in the database.

### 3. Calculate Match Score

```bash
curl -X POST "http://localhost:8000/api/matching/calculate/{resume_id}/{job_id}"
```

Returns:
```json
{
  "overall_score": 85.3,
  "keyword_score": 75.0,
  "semantic_score": 88.5,
  "experience_score": 90.0,
  "education_score": 80.0,
  "matched_skills": ["python", "fastapi", "docker"],
  "missing_skills": ["kubernetes", "aws"],
  "strengths": ["Strong match on 8 key skills"],
  "gaps": ["Missing 2 required skills"]
}
```

### 4. Get Top Matches

```bash
curl "http://localhost:8000/api/matching/matches/{resume_id}?min_score=70&limit=20"
```

Returns your top 20 job matches with scores above 70%.

### 5. Tailor Resume

```bash
curl -X POST "http://localhost:8000/api/matching/tailor" \\
  -H "Content-Type: application/json" \\
  -d '{
    "resume_id": 1,
    "job_id": 42
  }'
```

Returns AI-powered suggestions:
- Keywords to add
- Bullet points to rewrite
- Skills to emphasize
- Overall strategy

### 6. Track Applications

```bash
# Create application
curl -X POST "http://localhost:8000/api/applications/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "job_id": 42,
    "resume_id": 1,
    "notes": "Applied via company website"
  }'

# List all applications
curl "http://localhost:8000/api/applications/"

# Update status
curl -X PATCH "http://localhost:8000/api/applications/1/status?status=interview"
```

## Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   FastAPI   │────▶│ PostgreSQL  │     │   Qdrant    │
│   Backend   │     │   Database  │     │   Vector    │
│             │     │             │     │     DB      │
└──────┬──────┘     └─────────────┘     └──────┬──────┘
       │                                        │
       │            ┌─────────────┐            │
       └───────────▶│    Redis    │◀───────────┘
                    │   Cache +   │
                    │    Queue    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │   Celery    │
                    │   Workers   │
                    └─────────────┘
```

### Matching Algorithm

The match score is calculated using a weighted combination:

```
Overall Score = 0.30 × keyword_score
              + 0.40 × semantic_score
              + 0.15 × experience_score
              + 0.10 × education_score
              + 0.05 × location_score
```

- **Keyword Score**: Overlap between resume skills and required job skills
- **Semantic Score**: Cosine similarity between resume and job description embeddings
- **Experience Score**: How well experience level matches job requirements
- **Education Score**: Education background alignment
- **Location Score**: Location match bonus (remote jobs get full score)

## API Reference

Full API documentation available at `http://localhost:8000/docs` (Swagger UI)

### Key Endpoints

**Resumes**
- `POST /api/resumes/upload` - Upload and parse resume
- `GET /api/resumes/{id}` - Get resume details
- `GET /api/resumes/` - List all resumes

**Jobs**
- `POST /api/jobs/scrape` - Scrape jobs from job boards
- `GET /api/jobs/` - List jobs with pagination
- `GET /api/jobs/{id}` - Get job details

**Matching**
- `POST /api/matching/calculate/{resume_id}/{job_id}` - Calculate match score
- `GET /api/matching/matches/{resume_id}` - Get top matches
- `POST /api/matching/tailor` - Get tailoring suggestions
- `POST /api/matching/generate-tailored-resume` - Generate full tailored resume

**Applications**
- `POST /api/applications/` - Create application record
- `GET /api/applications/` - List applications
- `GET /api/applications/{id}` - Get application details
- `PATCH /api/applications/{id}/status` - Update status

## Configuration

Edit `backend/.env` to configure:

```bash
# Database
DATABASE_URL=postgresql://jobright:password@postgres:5432/jobright_db

# AI APIs (optional - for resume tailoring)
ANTHROPIC_API_KEY=your-key-here
OPENAI_API_KEY=your-key-here

# Job Scraping
JOBS_SCRAPE_INTERVAL_HOURS=6
MAX_JOBS_PER_SCRAPE=100

# ML Models
SENTENCE_TRANSFORMER_MODEL=all-MiniLM-L6-v2
```

## Development

### Project Structure
```
careerpilot/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI endpoints
│   │   ├── models/       # SQLAlchemy models
│   │   ├── services/     # Business logic
│   │   ├── ml/           # ML/matching logic
│   │   ├── scrapers/     # Job scraping
│   │   ├── config.py     # Configuration
│   │   ├── database.py   # Database setup
│   │   └── main.py       # FastAPI app
│   ├── tests/
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # (Future: React UI)
├── extension/            # (Future: Chrome extension)
└── docker-compose.yml
```

### Running Tests
```bash
cd backend
pytest tests/
```

### Adding New Job Sources

To add a new job scraping source, edit `backend/app/scrapers/job_scraper.py` and add your source to JobSpy configuration or implement a custom scraper.

## Chrome Extension (Coming Soon)

A Chrome extension will be added to provide:
- Auto-detect and autofill job application forms
- One-click application submission
- Screenshot confirmations
- Integration with backend API

## Roadmap

- [x] Resume parsing and storage
- [x] Job scraping from multiple sources
- [x] Semantic matching with embeddings
- [x] Match scoring algorithm
- [x] Resume tailoring with AI
- [x] Application tracking
- [ ] User authentication (JWT)
- [ ] React frontend UI
- [ ] Chrome extension for auto-apply
- [ ] Email notifications
- [ ] Cover letter generation
- [ ] Interview preparation tips
- [ ] Salary insights
- [ ] Company research integration

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - feel free to use this project for personal or commercial purposes.

## Acknowledgments

- [JobSpy](https://github.com/speedyapply/JobSpy) - Job scraping library
- [Sentence Transformers](https://www.sbert.net/) - Embedding models
- [Resume Matcher](https://github.com/srbhr/Resume-Matcher) - Inspiration for matching logic
- Anthropic Claude & OpenAI - AI-powered tailoring

## Disclaimer

This tool is for educational and personal use. Always review and verify any auto-generated content before using it in applications. Respect job board terms of service when scraping.

## Support

For issues, feature requests, or questions:
- Open an issue on GitHub
- Check the documentation at `/docs` endpoint
- Review the examples in this README

---

Built with ❤️ for job seekers everywhere
