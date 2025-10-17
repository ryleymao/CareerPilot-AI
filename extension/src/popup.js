// CareerPilot Popup Logic
const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', async () => {
  const loading = document.getElementById('loading');
  const matchView = document.getElementById('match-view');
  const noJob = document.getElementById('no-job');

  try {
    // Get current tab
    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });

    // Check if we're on a job page
    const isJobPage = tab.url.includes('job') ||
                       tab.url.includes('career') ||
                       tab.url.includes('apply');

    if (!isJobPage) {
      loading.style.display = 'none';
      noJob.style.display = 'block';
      return;
    }

    // Get job details from content script
    const response = await chrome.tabs.sendMessage(tab.id, { action: 'getJobDetails' });

    if (!response || !response.job) {
      loading.style.display = 'none';
      noJob.style.display = 'block';
      return;
    }

    // Calculate match score
    const matchData = await calculateMatch(response.job);

    // Display match data
    displayMatch(matchData);

    loading.style.display = 'none';
    matchView.style.display = 'block';

    // Set up button handlers
    setupButtons(tab, response.job, matchData);

  } catch (error) {
    console.error('Popup error:', error);
    loading.style.display = 'none';
    noJob.style.display = 'block';
  }
});

async function calculateMatch(jobDetails) {
  try {
    // Get user's resume
    const resumeRes = await fetch(`${API_URL}/api/resumes/`);
    const resumes = await resumeRes.json();

    if (!resumes || resumes.length === 0) {
      return {
        score: 0,
        matched: [],
        missing: [],
        message: 'Please upload your resume first!'
      };
    }

    const resume = resumes[0];

    // Try to find matching job in database
    const searchRes = await fetch(`${API_URL}/api/jobs/?search=${encodeURIComponent(jobDetails.title)}`);
    const jobs = await searchRes.json();

    let matchScore = null;

    if (jobs.jobs && jobs.jobs.length > 0) {
      // Calculate match with existing job
      const job = jobs.jobs[0];
      const matchRes = await fetch(`${API_URL}/api/matching/calculate/${resume.id}/${job.id}`, {
        method: 'POST'
      });
      matchScore = await matchRes.json();
    } else {
      // Quick estimate based on skills
      const resumeSkills = new Set((resume.skills || []).map(s => s.toLowerCase()));
      const jobSkills = extractSkills(jobDetails.description);

      const matched = jobSkills.filter(s => resumeSkills.has(s.toLowerCase()));
      const missing = jobSkills.filter(s => !resumeSkills.has(s.toLowerCase()));

      const score = jobSkills.length > 0 ?
        Math.round((matched.length / jobSkills.length) * 100) : 50;

      matchScore = {
        overall_score: score,
        matched_skills: matched,
        missing_skills: missing
      };
    }

    return matchScore;

  } catch (error) {
    console.error('Match calculation error:', error);
    return {
      score: 0,
      matched: [],
      missing: [],
      error: true
    };
  }
}

function extractSkills(text) {
  const commonSkills = [
    'python', 'java', 'javascript', 'typescript', 'react', 'node', 'sql',
    'aws', 'docker', 'kubernetes', 'git', 'agile', 'scrum', 'ci/cd'
  ];

  const textLower = text.toLowerCase();
  return commonSkills.filter(skill => textLower.includes(skill));
}

function displayMatch(matchData) {
  const scoreNumber = document.getElementById('score-number');
  const scoreCircle = document.getElementById('score-circle');
  const matchedSkills = document.getElementById('matched-skills');
  const missingSkills = document.getElementById('missing-skills');

  const score = matchData.overall_score || 0;

  // Display score
  scoreNumber.textContent = score;

  // Color code
  if (score >= 75) {
    scoreCircle.classList.add('high');
  } else if (score >= 50) {
    scoreCircle.classList.add('medium');
  } else {
    scoreCircle.classList.add('low');
  }

  // Display skills
  const matched = matchData.matched_skills || [];
  const missing = matchData.missing_skills || [];

  matchedSkills.textContent = matched.length > 0 ?
    matched.slice(0, 3).join(', ') + (matched.length > 3 ? '...' : '') :
    'None';

  missingSkills.textContent = missing.length > 0 ?
    missing.slice(0, 3).join(', ') + (missing.length > 3 ? '...' : '') :
    'None';
}

function setupButtons(tab, jobDetails, matchData) {
  document.getElementById('generate-resume').addEventListener('click', async () => {
    // Open CareerPilot UI to generate resume
    chrome.tabs.create({
      url: `http://localhost:3000/tailor?job=${encodeURIComponent(JSON.stringify(jobDetails))}`
    });
  });

  document.getElementById('auto-fill').addEventListener('click', async () => {
    // Trigger auto-fill
    await chrome.tabs.sendMessage(tab.id, { action: 'autoFill' });
    window.close();
  });

  document.getElementById('track-job').addEventListener('click', async () => {
    // Track the job
    await trackJob(jobDetails);
    alert('Job tracked! View in your dashboard.');
  });
}

async function trackJob(jobDetails) {
  try {
    const response = await fetch(`${API_URL}/api/applications/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        job_id: null,
        resume_id: 1,
        notes: `Tracked from: ${jobDetails.url}`,
        status: 'interested'
      })
    });
    return await response.json();
  } catch (error) {
    console.error('Track job error:', error);
  }
}
