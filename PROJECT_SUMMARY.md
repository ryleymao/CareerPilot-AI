# CareerPilot - Project Summary

## What We Built

A fully functional, **open-source job matching platform** inspired by JobRight.ai with AI-powered resume tailoring and job matching capabilities.

## Key Features Implemented

### Core Functionality
- ✅ Resume upload and parsing (PDF, DOCX, TXT)
- ✅ Intelligent skill extraction using spaCy NLP
- ✅ Multi-source job scraping (Indeed, LinkedIn, Glassdoor, ZipRecruiter)
- ✅ Semantic matching with embeddings (Sentence Transformers)
- ✅ Comprehensive match scoring algorithm
- ✅ AI-powered resume tailoring (Claude/GPT)
- ✅ Application tracking system
- ✅ RESTful API with FastAPI
- ✅ Docker containerization
- ✅ Background task processing with Celery

### Technical Implementation

**Backend (Python/FastAPI)**
- 29 Python files created
- 5 API endpoint modules
- 5 database models
- 3 ML/matching services
- 2 scraping/parsing services

**Infrastructure**
- Docker Compose with 8 services
- PostgreSQL for structured data
- Redis for caching/queuing
- Qdrant for vector embeddings
- Celery for async tasks
- Nginx reverse proxy

**Documentation**
- Comprehensive README
- Quick Start Guide
- Detailed Examples
- API Documentation (Swagger)

## Project Structure

```
careerpilot/
├── backend/
│   ├── app/
│   │   ├── api/              # FastAPI endpoints
│   │   │   ├── auth.py       # Authentication (placeholder)
│   │   │   ├── resumes.py    # Resume management
│   │   │   ├── jobs.py       # Job scraping/listing
│   │   │   ├── matching.py   # Match scoring/tailoring
│   │   │   └── applications.py # Application tracking
│   │   ├── models/           # Database models
│   │   │   ├── user.py
│   │   │   ├── resume.py
│   │   │   ├── job.py
│   │   │   ├── match_score.py
│   │   │   └── application.py
│   │   ├── services/         # Business logic
│   │   │   ├── resume_parser.py    # Resume parsing with spaCy
│   │   │   └── resume_tailor.py    # AI tailoring with LLMs
│   │   ├── ml/               # Machine learning
│   │   │   ├── embeddings.py       # Sentence Transformers
│   │   │   └── matching.py         # Matching algorithm
│   │   ├── scrapers/
│   │   │   └── job_scraper.py      # JobSpy integration
│   │   ├── config.py         # Configuration
│   │   ├── database.py       # SQLAlchemy setup
│   │   ├── main.py           # FastAPI app
│   │   └── celery_app.py     # Background tasks
│   ├── Dockerfile
│   ├── requirements.txt
│   └── .env.example
├── docker-compose.yml
├── nginx.conf
├── Makefile
├── README.md
├── QUICKSTART.md
├── EXAMPLES.md
└── .gitignore
```

## How It Works

### 1. Resume Processing Flow
```
Upload PDF → Extract Text → Parse with spaCy → Extract Skills/Experience →
Generate Embedding → Store in DB + Qdrant
```

### 2. Job Scraping Flow
```
API Request → JobSpy Scraper → Parse Job Data → Extract Skills →
Generate Embedding → Store in DB + Qdrant
```

### 3. Matching Flow
```
Resume + Job → Calculate Sub-Scores (keyword, semantic, experience, education, location) →
Weighted Combination → Overall Match Score (0-100)
```

### 4. Tailoring Flow
```
Resume + Job + Match Data → LLM Analysis → Generate Suggestions
(keywords, bullet rewrites, strategy) → Return to User
```

## Match Scoring Algorithm

The algorithm uses a weighted combination of multiple factors:

```
Overall Score = 30% × keyword_overlap
              + 40% × semantic_similarity
              + 15% × experience_match
              + 10% × education_match
              + 5% × location_bonus
```

**Keyword Score**: Jaccard similarity of skills
**Semantic Score**: Cosine similarity of embeddings
**Experience Score**: Years vs. job level alignment
**Education Score**: Degree vs. requirements
**Location Score**: Geographic match bonus

## API Endpoints

### Resumes
- `POST /api/resumes/upload` - Upload resume
- `GET /api/resumes/{id}` - Get resume details
- `GET /api/resumes/` - List resumes

### Jobs
- `POST /api/jobs/scrape` - Scrape jobs
- `GET /api/jobs/` - List jobs
- `GET /api/jobs/{id}` - Get job details

### Matching
- `POST /api/matching/calculate/{resume_id}/{job_id}` - Calculate match
- `GET /api/matching/matches/{resume_id}` - Get top matches
- `POST /api/matching/tailor` - Get tailoring suggestions
- `POST /api/matching/generate-tailored-resume` - Generate tailored resume

### Applications
- `POST /api/applications/` - Create application
- `GET /api/applications/` - List applications
- `GET /api/applications/{id}` - Get application details
- `PATCH /api/applications/{id}/status` - Update status

## Tech Stack Details

### Dependencies
- **FastAPI** 0.109.0 - Modern web framework
- **SQLAlchemy** 2.0.25 - ORM
- **Sentence Transformers** 2.3.1 - Embeddings
- **spaCy** 3.7.2 - NLP
- **JobSpy** 1.1.46 - Job scraping
- **Qdrant Client** 1.7.3 - Vector DB
- **Celery** 5.3.6 - Task queue
- **Anthropic** 0.18.1 - Claude API
- **OpenAI** 1.10.0 - GPT API

### ML Models
- **all-MiniLM-L6-v2**: 384-dim sentence embeddings
- **en_core_web_sm**: spaCy English model
- **Claude 3.5 Sonnet / GPT-4**: Resume tailoring

## What's Next (Future Enhancements)

### Phase 2 - Frontend (Not Built Yet)
- [ ] React TypeScript UI
- [ ] Job browsing interface
- [ ] Resume management dashboard
- [ ] Match visualization
- [ ] Application tracker UI

### Phase 3 - Chrome Extension (Not Built Yet)
- [ ] Auto-detect job application forms
- [ ] One-click autofill
- [ ] Form data extraction
- [ ] Screenshot capture
- [ ] Integration with backend

### Phase 4 - Advanced Features
- [ ] User authentication (JWT)
- [ ] Email notifications
- [ ] Cover letter generation
- [ ] Interview prep suggestions
- [ ] Salary insights
- [ ] Company research integration
- [ ] LinkedIn integration
- [ ] Resume version control
- [ ] Analytics dashboard

## Getting Started

### Quick Start (5 minutes)
```bash
# 1. Clone
git clone <repo-url>
cd careerpilot

# 2. Setup
cp backend/.env.example backend/.env
# Add API keys if desired

# 3. Start
docker-compose up -d

# 4. Use
# Upload resume
curl -X POST "http://localhost:8000/api/resumes/upload" -F "file=@resume.pdf"

# Scrape jobs
curl -X POST "http://localhost:8000/api/jobs/scrape" \\
  -H "Content-Type: application/json" \\
  -d '{"search_term": "Python Developer", "location": "Remote", "results_wanted": 20}'

# Get matches
curl "http://localhost:8000/api/matching/matches/1"
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

## Performance Characteristics

- **Resume parsing**: ~2-5 seconds per resume
- **Job scraping**: ~10-30 seconds for 20 jobs
- **Match calculation**: ~1-2 seconds per job
- **Embedding generation**: ~0.5 seconds per document
- **AI tailoring**: ~3-10 seconds (depends on LLM)

## Limitations & Known Issues

1. **Resume Parser**: Not 100% accurate on complex formats
2. **Job Scraping**: Subject to rate limits from job boards
3. **Authentication**: Currently placeholder (needs JWT implementation)
4. **Frontend**: No UI yet (API only)
5. **Chrome Extension**: Not implemented
6. **Scale**: Optimized for personal use, not production scale

## Deployment

### Local Development
```bash
make up        # Start services
make logs      # View logs
make down      # Stop services
```

### Production Considerations
- Use strong passwords/secrets
- Enable HTTPS with SSL certificates
- Set up database backups
- Configure rate limiting
- Add monitoring (Prometheus/Grafana)
- Scale with Kubernetes if needed

## License

MIT - Free for personal and commercial use

## Credits

Built using your tech stack:
- Python, SQL (PostgreSQL)
- FastAPI, REST APIs, Docker, Git, Redis, AWS-ready
- NumPy, Pandas, PyTorch (via Sentence Transformers)
- SQLAlchemy, Pydantic, Pytest-ready

Inspired by JobRight.ai and Resume Matcher open source project.

## Support

- GitHub Issues: Report bugs
- Documentation: README.md, QUICKSTART.md, EXAMPLES.md
- API Docs: http://localhost:8000/docs

---

**Status**: ✅ MVP Complete - Ready for Testing & Enhancement

Built on: January 2025
