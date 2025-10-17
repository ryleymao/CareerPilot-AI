# GitHub Setup Guide

## Quick Steps to Push to GitHub

### 1. Create Repository on GitHub

Go to https://github.com/new and create a new repository:

- **Repository name**: `jobright-clone`
- **Description**: `Open-source JobRight.ai alternative with AI-powered resume matching, tailoring, and job scraping`
- **Visibility**: ✅ Public (so others can use it)
- **Do NOT** check "Initialize with README" (we already have one)

Click **Create repository**

### 2. Push Code to GitHub

Run these commands in your terminal:

```bash
cd /Users/ryleymao/jobright-clone

# Add GitHub as remote
git remote add origin https://github.com/ryleymao/jobright-clone.git

# Push code
git push -u origin main
```

That's it! Your code will be live at:
**https://github.com/ryleymao/jobright-clone**

### 3. Add Your API Key (Don't commit it!)

After pushing to GitHub, add your Anthropic API key locally:

```bash
# Edit the .env file
nano backend/.env

# Add your key:
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Or use OpenAI instead:
OPENAI_API_KEY=sk-your-openai-key-here
```

**Important**: The `.env` file is in `.gitignore`, so your API key will NOT be pushed to GitHub.

### 4. Add Topics to Your Repo (Optional but Recommended)

On your GitHub repository page, click "⚙️ Settings" → "Topics" and add:
- `job-search`
- `resume-matching`
- `ai`
- `fastapi`
- `docker`
- `python`
- `resume-parser`
- `job-scraping`
- `machine-learning`
- `nlp`

This helps people discover your project!

### 5. Enable GitHub Issues and Discussions

In Settings:
- ✅ Enable Issues (for bug reports/feature requests)
- ✅ Enable Discussions (for community Q&A)

## Sharing Your Project

### Add Badges to README (Optional)

You can add these badges to make your README look professional. Add them at the top of README.md:

```markdown
# JobRight Clone - Open Source Job Matching Platform

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/python-3.11-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green.svg)
![Docker](https://img.shields.io/badge/docker-ready-blue.svg)
[![GitHub stars](https://img.shields.io/github/stars/ryleymao/jobright-clone.svg)](https://github.com/ryleymao/jobright-clone/stargazers)
```

### Share on Social Media

Tweet/post about it:
```
🚀 Just open-sourced my JobRight.ai alternative!

✅ AI-powered resume matching
✅ Job scraping (Indeed, LinkedIn, etc.)
✅ Resume tailoring with Claude/GPT
✅ Full Docker setup

Built with Python, FastAPI, PostgreSQL & ML

Free to use → https://github.com/ryleymao/jobright-clone

#OpenSource #JobSearch #AI #Python
```

### Submit to Directories

- Hacker News: https://news.ycombinator.com/submit
- Reddit: r/opensource, r/programming, r/Python, r/cscareerquestions
- Dev.to: Write a blog post about it
- Product Hunt: https://www.producthunt.com/

## Getting Your First Contributors

Add a `CONTRIBUTING.md` file:

```markdown
# Contributing

We welcome contributions! Here's how you can help:

## Getting Started
1. Fork the repo
2. Clone: `git clone https://github.com/YOUR_USERNAME/jobright-clone.git`
3. Create branch: `git checkout -b feature/your-feature`
4. Make changes
5. Test: `docker-compose up -d && pytest`
6. Commit: `git commit -m "Add your feature"`
7. Push: `git push origin feature/your-feature`
8. Open Pull Request

## Ideas for Contributions
- [ ] Add React frontend
- [ ] Build Chrome extension
- [ ] Improve resume parser accuracy
- [ ] Add more job sources
- [ ] Optimize matching algorithm
- [ ] Add tests
- [ ] Improve documentation
```

## Troubleshooting

### Git push asks for credentials

If prompted, use:
- **Username**: Your GitHub username
- **Password**: A Personal Access Token (not your password)

Get a token: https://github.com/settings/tokens
- Click "Generate new token (classic)"
- Select scope: `repo`
- Copy and use as password

### Alternative: Use SSH

```bash
# Generate SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add to GitHub: https://github.com/settings/keys

# Change remote URL
git remote set-url origin git@github.com:ryleymao/jobright-clone.git
```

## Next Steps After GitHub

1. **Star your own repo** ⭐ (shows engagement)
2. **Watch the repo** 👀 (get notifications)
3. **Add description and topics**
4. **Create first issue**: "Roadmap" or "Future Features"
5. **Share widely** on social media, forums, Discord servers

## Making Updates

After making changes:

```bash
git add .
git commit -m "Description of changes"
git push
```

That's it! Your project is now open source and ready for the world to use! 🎉

---

Need help? Open an issue at: https://github.com/ryleymao/jobright-clone/issues
