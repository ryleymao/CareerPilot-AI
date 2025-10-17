# CareerPilot Chrome Extension

AI-powered job application assistant that works on ANY job site!

## Features

✅ **Match Score on Any Job Page** - See how well you match before applying
✅ **One-Click Resume Generation** - AI tailors your resume instantly
✅ **Auto-Fill Applications** - Fill forms automatically with your data
✅ **Track External Applications** - Tracks even when you apply on company sites
✅ **Application History** - See all jobs you've applied to with match scores
✅ **Works Everywhere** - LinkedIn, Indeed, Greenhouse, company websites, etc.

## Installation

### For Development:
1. Open Chrome and go to `chrome://extensions/`
2. Enable "Developer mode" (top right)
3. Click "Load unpacked"
4. Select the `careerpilot/extension` folder
5. The ✈️ CareerPilot icon should appear in your extensions

### Usage:
1. Make sure CareerPilot backend is running: `docker-compose up`
2. Upload your resume at http://localhost:3000
3. Browse job listings on LinkedIn, Indeed, etc.
4. Click the CareerPilot extension icon to see your match %
5. Click "Generate Tailored Resume" or "Auto-Fill" to apply!

## Supported Platforms

- ✅ LinkedIn
- ✅ Indeed
- ✅ Greenhouse
- ✅ Lever
- ✅ Workday
- ✅ iCIMS
- ✅ Taleo
- ✅ SmartRecruiters
- ✅ Jobvite
- ✅ Any company career page!

## How It Works

1. **Detect Job Page**: Automatically detects when you're viewing a job
2. **Calculate Match**: Compares job requirements with your resume
3. **Show Score**: Displays match percentage (0-100%)
4. **Generate Resume**: AI tailors your resume for the specific job
5. **Auto-Fill**: Fills application forms with your information
6. **Track Application**: Saves to your application dashboard

## Privacy

- All data processed locally or on your self-hosted backend
- No data sent to third parties
- Resume data never leaves your control
- Open source - audit the code yourself!

## Troubleshooting

**Extension not working:**
- Make sure backend is running: `docker-compose up`
- Check console for errors: Right-click → Inspect → Console
- Reload the extension in chrome://extensions/

**Match score not showing:**
- Upload your resume first at http://localhost:3000
- Refresh the job page
- Make sure you're on a job listing page

**Auto-fill not working:**
- Some sites use custom forms that may not be supported yet
- Manual review is always recommended before submitting

## Development

Files:
- `manifest.json` - Extension configuration
- `src/content.js` - Runs on job pages
- `src/background.js` - Background service worker
- `src/popup.html` - Extension popup UI
- `src/popup.js` - Popup logic
- `src/styles.css` - Extension styles

To modify:
1. Edit the files
2. Go to chrome://extensions/
3. Click the reload icon on CareerPilot
4. Refresh the job page to test

## Coming Soon

- [ ] Browser action badge with match score
- [ ] One-click apply to multiple jobs
- [ ] Cover letter generation
- [ ] Interview prep tips based on job
- [ ] Salary insights
- [ ] Company research integration

---

Built with ❤️ for job seekers everywhere
