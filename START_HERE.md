# 🚀 START USING CAREERPILOT NOW - 5 Minute Setup!

Your AI job search copilot is ready! Here's how to start applying to jobs TODAY.

## Step 1: Start the Backend (2 minutes)

```bash
cd /Users/ryleymao/careerpilot

# Start all services
docker-compose up -d

# Wait 30 seconds for services to start
# Check status
docker-compose ps
```

✅ **Backend running at**: http://localhost:8000

## Step 2: Upload Your Resume (1 minute)

```bash
# Upload your resume
curl -X POST "http://localhost:8000/api/resumes/upload" \
  -F "file=@/path/to/your_resume.pdf"

# Example:
curl -X POST "http://localhost:8000/api/resumes/upload" \
  -F "file=@~/Desktop/resume.pdf"
```

✅ **Resume uploaded!** The AI has now parsed your skills, experience, and education.

## Step 3: Scrape Some Jobs (1 minute)

```bash
# Scrape jobs matching your profile
curl -X POST "http://localhost:8000/api/jobs/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "YOUR JOB TITLE HERE",
    "location": "Remote",
    "results_wanted": 50
  }'

# Examples:
# Software Engineer: "search_term": "Software Engineer"
# Marketing Manager: "search_term": "Marketing Manager"
# Data Analyst: "search_term": "Data Analyst"
# Product Manager: "search_term": "Product Manager"
```

✅ **Jobs scraped!** From LinkedIn, Indeed, Glassdoor, ZipRecruiter

## Step 4: Install Chrome Extension (1 minute)

1. Open Chrome and go to: `chrome://extensions/`
2. Enable **"Developer mode"** (toggle in top right)
3. Click **"Load unpacked"**
4. Navigate to: `/Users/ryleymao/careerpilot/extension`
5. Click **"Select"**

✅ **Extension installed!** You'll see the ✈️ icon in your toolbar

## 🎉 YOU'RE READY! Start Applying:

### Method 1: Use the Extension (EASIEST!)

1. Go to **LinkedIn**, **Indeed**, or **any job site**
2. Open any job listing
3. Click the **✈️ CareerPilot** extension icon
4. See your **match score %**
5. Click **"Generate Tailored Resume"** or **"Auto-Fill Application"**
6. Apply!

### Method 2: View Your Top Matches

```bash
# See your top matches
curl "http://localhost:8000/api/matching/matches/1?min_score=70&limit=10"
```

This shows jobs ranked by how well they match YOU!

### Method 3: Get Tailoring Suggestions

```bash
# Get AI suggestions for a specific job
curl -X POST "http://localhost:8000/api/matching/tailor" \
  -H "Content-Type: application/json" \
  -d '{"resume_id": 1, "job_id": 5}'
```

The AI will tell you:
- Keywords to add
- Bullet points to rewrite
- Skills to emphasize

## 📊 Track Your Applications

```bash
# See all your applications
curl "http://localhost:8000/api/applications/"
```

The extension **automatically tracks** every application with:
- Match score
- Company & job title
- Application status
- Date applied

## 🎯 Pro Tips:

1. **Use the extension on EVERY job** - it works on LinkedIn, Indeed, company websites, everywhere!

2. **Look for high match scores** - Focus on jobs 75%+ match

3. **Let AI tailor your resume** - Click "Generate Tailored Resume" for each job

4. **Auto-fill saves time** - The extension fills forms automatically

5. **Review before submitting** - Always check the autofilled data

## 🔥 Advanced: Batch Apply

Want to apply to 20 jobs at once?

```bash
# Get your top 20 matches
curl "http://localhost:8000/api/matching/matches/1?min_score=80&limit=20"

# For each job, generate tailored resume and apply!
```

## 🐛 Troubleshooting

**Extension not working?**
```bash
# Restart backend
docker-compose restart backend
```

**No match scores showing?**
- Make sure you uploaded your resume (Step 2)
- Refresh the job page

**Jobs too old?**
- They're automatically filtered if >90 days old
- Lower the freshness threshold in config if needed

**Want different jobs?**
```bash
# Scrape different titles/locations
curl -X POST "http://localhost:8000/api/jobs/scrape" \
  -H "Content-Type: application/json" \
  -d '{
    "search_term": "Product Manager",
    "location": "New York, NY",
    "results_wanted": 50
  }'
```

## 🎊 YOU'RE ALL SET!

**CareerPilot is working for YOU 24/7:**
- ✅ Matching you to jobs
- ✅ Tailoring your resume
- ✅ Filling applications
- ✅ Tracking everything

**Now go apply to some jobs and get those offers!** 🚀

---

## Quick Reference

- **Backend API**: http://localhost:8000/docs
- **View Jobs**: `curl localhost:8000/api/jobs/`
- **View Matches**: `curl localhost:8000/api/matching/matches/1`
- **View Applications**: `curl localhost:8000/api/applications/`
- **Extension**: Click ✈️ icon on any job page

Need help? Check `README.md` or open an issue on GitHub!

**Let's get you hired!** 💼✨
