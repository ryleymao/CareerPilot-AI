# 🎬 CareerPilot Demo Guide

Complete walkthrough to demo all features!

## 🚀 Step 1: Start the System

```bash
# Make sure Docker is running first!
# On Mac: Open Docker Desktop

cd /Users/ryleymao/careerpilot

# Start all services
docker-compose up -d --build

# Wait 30-60 seconds for services to start
# Check status
docker-compose ps
```

**What's starting:**
- ✅ PostgreSQL database
- ✅ Redis cache
- ✅ Qdrant vector database
- ✅ FastAPI backend (port 8000)
- ✅ React frontend (port 3000)
- ✅ Celery workers
- ✅ Nginx proxy

## 🌐 Step 2: Open the Frontend

Open your browser to: **http://localhost:3000**

You should see the beautiful CareerPilot dashboard!

### Dashboard Features:
- **Stats cards**: Resume status, applications count, pending jobs
- **Quick actions**: Upload resume, browse jobs, track applications
- **Top job matches**: Your best-fitting jobs (after resume upload)
- **Tips for success**: Helpful guidance

## 📄 Step 3: Upload Your Resume

1. Click **"Resume"** in the sidebar
2. **Drag and drop** your resume PDF/DOC/DOCX
3. Watch as AI analyzes it in real-time!

**What happens:**
- ✨ AI extracts your name, email, phone
- 🎯 Identifies all your skills
- 📊 Calculates years of experience
- 🎓 Parses education history
- 💾 Stores everything in the database

**Result:** Beautiful display of your parsed resume with:
- Experience years count
- All detected skills as tags
- Education details
- Contact information

## 🔍 Step 4: Discover Jobs with AI

1. Click **"Jobs"** in the sidebar
2. Enter a job title in the search box (e.g., "Software Engineer", "Marketing Manager")
3. Click **"🤖 AI Discover Jobs"**

**What happens:**
- 🤖 AI searches across LinkedIn, Indeed, ZipRecruiter, Glassdoor
- ✅ Filters out jobs older than 14 days
- 🚫 Removes spam and scam postings
- ⭐ Quality scores each job (>70% required)
- 🔄 Deduplicates results
- 📊 Calculates YOUR match score for each job

**Result:** List of high-quality jobs with:
- Match percentage (green = 75%+, yellow = 50-74%, red = <50%)
- Company and location
- Matched skills (green tags)
- Missing skills (red tags)
- Posted date
- Salary range
- "View Job" and "Generate Resume" buttons

## 🎯 Step 5: View Your Match Scores

After jobs are discovered, each job card shows:

**High Match (75%+)**: Green badge
- You have most required skills
- Great fit for your experience level
- **Action**: Apply immediately!

**Medium Match (50-74%)**: Yellow badge
- You have some required skills
- May need to highlight transferable skills
- **Action**: Consider tailoring resume

**Low Match (<50%)**: Red badge
- Missing many required skills
- May not be the best fit
- **Action**: Probably skip unless really interested

## 📝 Step 6: Track Applications

1. Click **"Applications"** in the sidebar
2. See all your job applications with status

**Stats shown:**
- Total applications
- Submitted count
- Interviews scheduled
- Offers received
- Rejected count

**For each application:**
- Job title and company
- Application date
- Current status (color-coded)
- Auto-applied badge if used extension
- Update status dropdown
- Notes field

**Update statuses:**
- Interested → Submitted → Interview → Offered → Accepted
- Or mark as Rejected

## 🎨 Step 7: Use Chrome Extension

### Install Extension:
1. Go to `chrome://extensions/`
2. Enable "Developer mode"
3. Click "Load unpacked"
4. Select `/Users/ryleymao/careerpilot/extension`

### Use on Job Sites:
1. **Go to LinkedIn, Indeed, or any job site**
2. **Open a job listing**
3. **Click the ✈️ CareerPilot extension icon**

**Extension shows:**
- ⭐ Your match score %
- ✅ Matched skills
- ❌ Missing skills
- 📅 Job age

**Actions available:**
- **Generate Tailored Resume**: AI customizes your resume for this specific job
- **Auto-Fill Application**: Fills forms with your data
- **Track This Job**: Saves to your dashboard

### Extension works on:
- LinkedIn
- Indeed
- Greenhouse
- Lever
- Workday
- iCIMS
- Taleo
- SmartRecruiters
- Jobvite
- Any company career page!

## 🔥 Step 8: Demo the AI Features

### Show AI Job Discovery vs Basic Scrapers:

**Old way (Indeed/LinkedIn):**
- Shows jobs posted 90 days ago
- Includes spam postings
- No quality filtering
- Duplicates everywhere

**CareerPilot AI way:**
- ✅ Only last 14 days
- ✅ Spam detection
- ✅ Quality scoring (>70%)
- ✅ Deduplication
- ✅ Match percentage calculated

### Show Universal Profession Support:

Search for different job types:
- "Software Engineer" ✅
- "Marketing Manager" ✅
- "Registered Nurse" ✅
- "High School Teacher" ✅
- "Financial Analyst" ✅
- "Graphic Designer" ✅

All work! Not just tech jobs.

## 📊 Step 9: API Demo (Optional)

Open **http://localhost:8000/docs** for interactive API docs!

### Try these endpoints:

**Upload Resume:**
```bash
curl -X POST "http://localhost:8000/api/resumes/upload" \
  -F "file=@/path/to/resume.pdf"
```

**AI Job Discovery:**
```bash
curl -X POST "http://localhost:8000/api/jobs/discover" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Product Manager",
    "location": "Remote",
    "results_wanted": 50
  }'
```

**Get Top Matches:**
```bash
curl "http://localhost:8000/api/matching/matches/1?min_score=75&limit=10"
```

**Generate Tailored Resume:**
```bash
curl -X POST "http://localhost:8000/api/matching/tailor" \
  -H "Content-Type: application/json" \
  -d '{"resume_id": 1, "job_id": 5}'
```

## 🎯 Key Demo Points

### 1. **Beautiful UI**
- Modern, clean design with gradients
- Smooth animations and transitions
- Responsive layout
- Easy navigation

### 2. **Smart AI**
- Only fresh jobs (14 days max)
- Spam/scam detection
- Quality scoring
- Match percentage calculation

### 3. **Universal Support**
- Works for ALL job types
- Not just tech/software engineering
- 100+ skills across industries

### 4. **Chrome Extension**
- Works on ANY job site
- Real-time match scores
- Auto-fill applications
- External application tracking

### 5. **FREE & Open Source**
- No API costs (uses Ollama)
- Self-hosted
- Fully customizable
- Share with anyone!

## 🐛 Troubleshooting

**Frontend not loading?**
```bash
docker-compose logs frontend
```

**Backend errors?**
```bash
docker-compose logs backend
```

**Database issues?**
```bash
docker-compose restart postgres
docker-compose logs postgres
```

**Rebuild everything:**
```bash
docker-compose down -v
docker-compose up -d --build
```

## 🎊 Demo Script

Here's a 5-minute demo script:

**Minute 1:** "This is CareerPilot, an open-source AI job search assistant. Unlike JobRight.ai which costs money, this is completely free and you own all your data."

**Minute 2:** "Let me upload a resume... [drag-drop resume] See how AI instantly parses it? It found 15 skills, 5 years experience, and my education."

**Minute 3:** "Now let's find some jobs... [enter 'Software Engineer', click AI Discover] Notice it says 'AI Searching'? That's because it's not just scraping - it's validating that jobs are fresh and legitimate."

**Minute 4:** "Look at these results! Each has a match score. This 85% match is perfect - I have all the required skills. This 60% match is missing a few skills, so maybe I'd skip it."

**Minute 5:** "And here's the best part - [show extension] I can browse LinkedIn or Indeed, and CareerPilot tells me my match score right there! Then auto-fill the application."

**Wrap up:** "It's open source, dockerized, and works for any profession. Software engineers, teachers, nurses - anyone can use it!"

## 📈 Features to Highlight

✅ Drag-and-drop resume upload
✅ AI resume parsing
✅ Smart job discovery (fresh jobs only!)
✅ Spam detection
✅ Match score calculation
✅ Chrome extension (works everywhere!)
✅ Auto-fill applications
✅ Application tracking
✅ Universal profession support
✅ FREE with Ollama
✅ Beautiful modern UI
✅ Fully dockerized
✅ Open source

---

**Now go wow everyone with your AI-powered job search copilot!** ✈️🎉
