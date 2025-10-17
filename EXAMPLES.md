# Usage Examples

Real-world examples of using JobRight Clone.

## Example 1: Full Workflow - Python Developer

### Step 1: Upload Resume
```bash
curl -X POST "http://localhost:8000/api/resumes/upload" \\
  -F "file=@john_doe_resume.pdf"
```

**Response:**
```json
{
  "resume_id": 1,
  "filename": "john_doe_resume.pdf",
  "parsed_data": {
    "name": "John Doe",
    "email": "john@example.com",
    "skills": ["python", "fastapi", "postgresql", "docker", "aws"],
    "experience_years": 5,
    "education": [{"degree": "bachelor", "field": "computer science"}]
  }
}
```

### Step 2: Scrape Jobs
```bash
curl -X POST "http://localhost:8000/api/jobs/scrape" \\
  -H "Content-Type: application/json" \\
  -d '{
    "search_term": "Senior Python Developer",
    "location": "Remote",
    "results_wanted": 50
  }'
```

**Response:**
```json
{
  "message": "Jobs scraped successfully",
  "added": 45,
  "updated": 5,
  "total": 50
}
```

### Step 3: Get Top Matches
```bash
curl "http://localhost:8000/api/matching/matches/1?min_score=70"
```

**Response:**
```json
{
  "resume_id": 1,
  "matches": [
    {
      "job_id": 23,
      "title": "Senior Python Backend Engineer",
      "company": "Tech Corp",
      "location": "Remote",
      "overall_score": 92.5,
      "matched_skills": ["python", "fastapi", "postgresql", "docker"],
      "missing_skills": ["kubernetes"],
      "strengths": ["Strong match on 8 key skills", "Experience level matches"],
      "gaps": ["Missing 1 required skill: kubernetes"]
    },
    {
      "job_id": 17,
      "title": "Python Full Stack Developer",
      "company": "StartupXYZ",
      "location": "Remote",
      "overall_score": 87.3,
      "matched_skills": ["python", "postgresql", "aws"],
      "missing_skills": ["react", "typescript"],
      "strengths": ["Backend skills strong match"],
      "gaps": ["Frontend skills not present"]
    }
  ]
}
```

### Step 4: Calculate Detailed Match
```bash
curl -X POST "http://localhost:8000/api/matching/calculate/1/23"
```

**Response:**
```json
{
  "resume_id": 1,
  "job_id": 23,
  "job_title": "Senior Python Backend Engineer",
  "company": "Tech Corp",
  "overall_score": 92.5,
  "keyword_score": 88.0,
  "semantic_score": 94.2,
  "experience_score": 95.0,
  "education_score": 90.0,
  "location_score": 100.0,
  "matched_skills": ["python", "fastapi", "postgresql", "docker", "aws", "redis", "celery"],
  "missing_skills": ["kubernetes"],
  "strengths": [
    "Strong match on 7 key skills: python, fastapi, postgresql, docker, aws",
    "Experience level matches job requirements",
    "Educational background aligns well"
  ],
  "gaps": [
    "Missing 1 required skill: kubernetes"
  ]
}
```

### Step 5: Get Tailoring Suggestions
```bash
curl -X POST "http://localhost:8000/api/matching/tailor" \\
  -H "Content-Type: application/json" \\
  -d '{"resume_id": 1, "job_id": 23}'
```

**Response:**
```json
{
  "resume_id": 1,
  "job_id": 23,
  "suggestions": {
    "keyword_suggestions": ["kubernetes", "microservices", "CI/CD"],
    "bullet_rewrites": [
      {
        "original": "Built REST APIs using Python",
        "suggested": "Architected and deployed microservices-based REST APIs using Python, FastAPI, and Docker, serving 1M+ requests/day"
      },
      {
        "original": "Managed database operations",
        "suggested": "Optimized PostgreSQL database operations and implemented Redis caching, reducing query times by 60%"
      }
    ],
    "skills_to_highlight": ["python", "fastapi", "postgresql", "docker", "aws"],
    "overall_strategy": "Emphasize your microservices experience, highlight Docker/containerization skills, and mention any Kubernetes exposure or willingness to learn. Frame your AWS experience prominently."
  }
}
```

### Step 6: Generate Tailored Resume
```bash
curl -X POST "http://localhost:8000/api/matching/generate-tailored-resume" \\
  -H "Content-Type: application/json" \\
  -d '{"resume_id": 1, "job_id": 23}'
```

**Response:**
```json
{
  "resume_id": 1,
  "job_id": 23,
  "tailored_resume": "JOHN DOE\\nSenior Backend Engineer\\n\\n[Tailored resume with optimized keywords and phrases...]"
}
```

### Step 7: Track Application
```bash
curl -X POST "http://localhost:8000/api/applications/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "job_id": 23,
    "resume_id": 1,
    "notes": "Applied via LinkedIn on Jan 15, 2025. Used tailored resume version 2."
  }'
```

**Response:**
```json
{
  "application_id": 1,
  "job_id": 23,
  "status": "pending",
  "applied_at": "2025-01-15T10:30:00Z"
}
```

## Example 2: Batch Job Search Across Multiple Titles

```bash
# Search for multiple job titles
for title in "Python Developer" "Backend Engineer" "Full Stack Developer"; do
  curl -X POST "http://localhost:8000/api/jobs/scrape" \\
    -H "Content-Type: application/json" \\
    -d "{
      \\"search_term\\": \\"$title\\",
      \\"location\\": \\"Remote\\",
      \\"results_wanted\\": 30
    }"
  sleep 2  # Rate limiting
done
```

## Example 3: Filter High-Quality Matches

```bash
# Get only matches above 85% with at least 15 matched skills
curl "http://localhost:8000/api/matching/matches/1?min_score=85&limit=5"
```

## Example 4: Application Tracking Dashboard

```bash
# Get all applications
curl "http://localhost:8000/api/applications/"

# Update status after interview
curl -X PATCH "http://localhost:8000/api/applications/1/status?status=interview"

# Add notes
curl -X POST "http://localhost:8000/api/applications/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "job_id": 23,
    "resume_id": 1,
    "notes": "First round interview scheduled for Jan 20. Technical round with Sarah (CTO)."
  }'
```

## Example 5: Multi-Resume Strategy

```bash
# Upload specialized resume for ML roles
curl -X POST "http://localhost:8000/api/resumes/upload" \\
  -F "file=@john_doe_ml_resume.pdf"

# Upload generalist full-stack resume
curl -X POST "http://localhost:8000/api/resumes/upload" \\
  -F "file=@john_doe_fullstack_resume.pdf"

# Compare matches for both resumes
curl "http://localhost:8000/api/matching/matches/1"
curl "http://localhost:8000/api/matching/matches/2"
```

## Example 6: Location-Based Search

```bash
# Search in specific cities
for location in "New York, NY" "San Francisco, CA" "Austin, TX" "Remote"; do
  curl -X POST "http://localhost:8000/api/jobs/scrape" \\
    -H "Content-Type: application/json" \\
    -d "{
      \\"search_term\\": \\"Python Developer\\",
      \\"location\\": \\"$location\\",
      \\"results_wanted\\": 25
    }"
done
```

## Example 7: Using Python SDK

```python
import requests

BASE_URL = "http://localhost:8000"

# Upload resume
with open("resume.pdf", "rb") as f:
    response = requests.post(
        f"{BASE_URL}/api/resumes/upload",
        files={"file": f}
    )
    resume_id = response.json()["resume_id"]

# Scrape jobs
response = requests.post(
    f"{BASE_URL}/api/jobs/scrape",
    json={
        "search_term": "Python Developer",
        "location": "Remote",
        "results_wanted": 50
    }
)

# Get matches
response = requests.get(
    f"{BASE_URL}/api/matching/matches/{resume_id}",
    params={"min_score": 70, "limit": 20}
)

matches = response.json()["matches"]

# Apply to top 5 matches
for match in matches[:5]:
    job_id = match["job_id"]

    # Get tailoring suggestions
    suggestions = requests.post(
        f"{BASE_URL}/api/matching/tailor",
        json={"resume_id": resume_id, "job_id": job_id}
    ).json()

    print(f"Job: {match['title']} at {match['company']}")
    print(f"Score: {match['overall_score']}%")
    print(f"Suggestions: {suggestions['suggestions']['overall_strategy']}")
    print("-" * 50)
```

## Example 8: Weekly Job Alerts Automation

```bash
#!/bin/bash
# weekly_job_scrape.sh

# Scrape jobs weekly
curl -X POST "http://localhost:8000/api/jobs/scrape" \\
  -H "Content-Type: application/json" \\
  -d '{
    "search_term": "Python Developer",
    "location": "Remote",
    "results_wanted": 100
  }'

# Get new high-quality matches
RESUME_ID=1
curl "http://localhost:8000/api/matching/matches/${RESUME_ID}?min_score=80" \\
  | jq '.matches[] | {title, company, score: .overall_score}'

# Run weekly with cron:
# 0 9 * * 1 /path/to/weekly_job_scrape.sh
```

## Tips & Best Practices

1. **Start with high-quality resume**: Better parsing = better matches
2. **Use specific job titles**: "Senior Python Backend Engineer" > "Developer"
3. **Cast a wide net initially**: Scrape 50-100 jobs per search
4. **Filter aggressively**: Focus on matches above 75%
5. **Tailor for top matches**: Use AI tailoring for jobs 85%+
6. **Track everything**: Even rejected applications (learn from patterns)
7. **Update resume regularly**: Re-upload when you gain new skills
8. **Experiment with keywords**: Try variations of job titles

## Troubleshooting Examples

### Debug low match scores
```bash
# Get detailed breakdown
curl -X POST "http://localhost:8000/api/matching/calculate/1/{job_id}" \\
  | jq '.gaps'

# Shows exactly what's missing
```

### Check job data quality
```bash
# View raw job details
curl "http://localhost:8000/api/jobs/{job_id}" \\
  | jq '.required_skills'
```

### Verify resume parsing
```bash
# Check what was extracted
curl "http://localhost:8000/api/resumes/1" \\
  | jq '.parsed_data'
```

For more examples, check the [API documentation](http://localhost:8000/docs).
