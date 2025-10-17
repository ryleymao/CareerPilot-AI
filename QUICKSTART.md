# Quick Start Guide

Get up and running with JobRight Clone in 5 minutes!

## Prerequisites

- Docker Desktop installed
- 8GB+ RAM
- (Optional) Anthropic or OpenAI API key

## Step-by-Step Setup

### 1. Clone and Setup (1 minute)

```bash
# Clone repository
git clone https://github.com/yourusername/jobright-clone.git
cd jobright-clone

# Copy environment file
cp backend/.env.example backend/.env

# (Optional) Add your AI API key for resume tailoring
# Edit backend/.env and add:
# ANTHROPIC_API_KEY=your-key-here
```

### 2. Start Services (2 minutes)

```bash
# Start all containers
docker-compose up -d

# Wait for services to be ready (30-60 seconds)
# Check status
docker-compose ps

# View logs
docker-compose logs -f backend
```

### 3. Upload Resume (30 seconds)

```bash
# Upload your resume
curl -X POST "http://localhost:8000/api/resumes/upload" \\
  -F "file=@/path/to/your_resume.pdf"

# Save the resume_id from response
# Example response: {"resume_id": 1, ...}
```

### 4. Scrape Jobs (1 minute)

```bash
# Scrape Python Developer jobs in SF
curl -X POST "http://localhost:8000/api/jobs/scrape" \\
  -H "Content-Type: application/json" \\
  -d '{
    "search_term": "Python Developer",
    "location": "San Francisco, CA",
    "results_wanted": 20
  }'

# Wait for scraping to complete
# This will return immediately with job counts
```

### 5. Find Matches (30 seconds)

```bash
# Get top matches for your resume
# Replace {resume_id} with your resume_id from step 3
curl "http://localhost:8000/api/matching/matches/1?min_score=60&limit=10"

# You'll see jobs ranked by match score!
```

## Next Steps

### View Job Details
```bash
curl "http://localhost:8000/api/jobs/{job_id}"
```

### Calculate Detailed Match Score
```bash
curl -X POST "http://localhost:8000/api/matching/calculate/1/{job_id}"
```

### Get Resume Tailoring Suggestions
```bash
curl -X POST "http://localhost:8000/api/matching/tailor" \\
  -H "Content-Type: application/json" \\
  -d '{
    "resume_id": 1,
    "job_id": 5
  }'
```

### Track Application
```bash
curl -X POST "http://localhost:8000/api/applications/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "job_id": 5,
    "resume_id": 1,
    "notes": "Applied on 2025-01-15"
  }'
```

## Explore the API

Open your browser and visit:
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

The Swagger UI provides an interactive interface to test all endpoints!

## Common Issues

### Services won't start
```bash
# Check if ports are already in use
docker-compose down
docker-compose up -d
```

### Resume parsing fails
- Ensure your resume is in PDF or DOCX format
- Check file size (max 10MB)
- Try a different resume file

### Job scraping returns no results
- Try different search terms or locations
- Check if job boards are accessible
- View backend logs: `docker-compose logs backend`

### Out of memory
- Increase Docker memory limit to 8GB+
- Stop other applications

## Stopping the Application

```bash
# Stop all services
docker-compose down

# Stop and remove all data
docker-compose down -v
```

## Production Deployment

For production use:
1. Change `SECRET_KEY` in `.env`
2. Use strong database passwords
3. Enable HTTPS with proper SSL certificates
4. Set up proper backup for PostgreSQL
5. Configure rate limiting
6. Add authentication (JWT)

## Getting Help

- Check the full [README.md](README.md)
- View API docs at http://localhost:8000/docs
- Open an issue on GitHub

Happy job hunting! 🎯
