// CareerPilot Content Script - Auto-fill job applications
console.log('🚀 CareerPilot extension loaded!');

const API_URL = 'http://localhost:8000';

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'getJobDetails') {
    const jobDetails = extractJobDetails();
    sendResponse({ job: jobDetails });
  } else if (request.action === 'autoFill') {
    autoFillApplication().then(() => sendResponse({ success: true }));
    return true; // Keep channel open for async response
  }
  return true;
});

// Inject CareerPilot button on job application pages
function injectCareerPilotButton() {
  // Don't inject if already exists
  if (document.getElementById('careerpilot-autofill-btn')) return;

  // Detect if we're on an application page
  const isApplicationPage =
    window.location.href.includes('apply') ||
    window.location.href.includes('application') ||
    document.querySelector('form[class*="application"]') ||
    document.querySelector('input[name*="resume"]') ||
    document.querySelector('input[type="file"]');

  if (!isApplicationPage) return;

  // Create floating button
  const button = document.createElement('button');
  button.id = 'careerpilot-autofill-btn';
  button.innerHTML = '✈️ CareerPilot Auto-Fill';
  button.className = 'careerpilot-btn';

  button.onclick = async () => {
    button.innerHTML = '⏳ Filling...';
    button.disabled = true;

    try {
      await autoFillApplication();
      button.innerHTML = '✅ Filled!';
      setTimeout(() => {
        button.innerHTML = '✈️ CareerPilot Auto-Fill';
        button.disabled = false;
      }, 2000);
    } catch (error) {
      console.error('CareerPilot error:', error);
      button.innerHTML = '❌ Error';
      button.disabled = false;
    }
  };

  document.body.appendChild(button);
}

// Auto-fill the application form
async function autoFillApplication() {
  // Get user's resume data from backend
  const resumeData = await fetchResumeData();

  if (!resumeData) {
    alert('Please upload your resume to CareerPilot first!');
    window.open('http://localhost:3000', '_blank');
    return;
  }

  // Extract job details from current page
  const jobDetails = extractJobDetails();

  // Get tailored resume for this job
  const tailoredData = await getTailoredResume(resumeData.id, jobDetails);

  // Fill form fields
  fillFormFields(resumeData, tailoredData);

  // Take screenshot for tracking
  await takeScreenshot();

  // Track application
  await trackApplication(jobDetails);
}

// Fetch user's resume from backend
async function fetchResumeData() {
  try {
    const response = await fetch(`${API_URL}/api/resumes/`);
    const data = await response.json();
    return data[0]; // Get first resume
  } catch (error) {
    console.error('Failed to fetch resume:', error);
    return null;
  }
}

// Extract job details from page
function extractJobDetails() {
  const title =
    document.querySelector('h1')?.textContent ||
    document.querySelector('[class*="job-title"]')?.textContent ||
    document.title;

  const company =
    document.querySelector('[class*="company"]')?.textContent ||
    document.querySelector('[class*="employer"]')?.textContent ||
    '';

  const description =
    document.querySelector('[class*="description"]')?.textContent ||
    document.querySelector('[class*="job-details"]')?.textContent ||
    document.body.innerText.substring(0, 5000);

  return {
    title: title?.trim(),
    company: company?.trim(),
    description: description?.trim(),
    url: window.location.href
  };
}

// Get tailored resume from backend
async function getTailoredResume(resumeId, jobDetails) {
  // First, try to match with existing job in database
  try {
    const searchResponse = await fetch(`${API_URL}/api/jobs/?search=${encodeURIComponent(jobDetails.title)}`);
    const jobs = await searchResponse.json();

    if (jobs.jobs && jobs.jobs.length > 0) {
      const jobId = jobs.jobs[0].id;

      // Get tailoring suggestions
      const tailorResponse = await fetch(`${API_URL}/api/matching/tailor`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ resume_id: resumeId, job_id: jobId })
      });

      return await tailorResponse.json();
    }
  } catch (error) {
    console.log('Using generic resume data');
  }

  return null;
}

// Fill form fields with resume data
function fillFormFields(resumeData, tailoredData) {
  const parsed = resumeData.parsed_data || {};

  // Common field mappings
  const fieldMappings = {
    // Name fields
    name: parsed.name || '',
    firstname: parsed.name?.split(' ')[0] || '',
    lastname: parsed.name?.split(' ').slice(1).join(' ') || '',
    fullname: parsed.name || '',

    // Contact fields
    email: parsed.email || '',
    phone: parsed.phone || '',
    mobile: parsed.phone || '',

    // LinkedIn
    linkedin: parsed.linkedin || '',

    // Experience
    experience: resumeData.experience_years || '',
    years: resumeData.experience_years || '',
  };

  // Fill text inputs
  document.querySelectorAll('input[type="text"], input[type="email"], input[type="tel"]').forEach(input => {
    const fieldName = (input.name || input.id || input.placeholder || '').toLowerCase();

    for (const [key, value] of Object.entries(fieldMappings)) {
      if (fieldName.includes(key) && value) {
        input.value = value;
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        console.log(`Filled ${fieldName} with ${value}`);
      }
    }
  });

  // Fill textareas (cover letter, additional info)
  document.querySelectorAll('textarea').forEach(textarea => {
    const fieldName = (textarea.name || textarea.id || textarea.placeholder || '').toLowerCase();

    if (fieldName.includes('cover') || fieldName.includes('letter')) {
      if (tailoredData?.cover_letter) {
        textarea.value = tailoredData.cover_letter;
      } else {
        textarea.value = `I am excited to apply for this position. My ${resumeData.experience_years} years of experience in ${resumeData.skills?.slice(0, 3).join(', ')} make me a strong candidate.`;
      }
      textarea.dispatchEvent(new Event('input', { bubbles: true }));
    }
  });

  // Handle file uploads (resume)
  document.querySelectorAll('input[type="file"]').forEach(input => {
    const fieldName = (input.name || input.id || '').toLowerCase();
    if (fieldName.includes('resume') || fieldName.includes('cv')) {
      // Show message about manual upload
      const label = input.closest('label') || input.parentElement;
      if (label) {
        label.style.border = '3px solid #4CAF50';
        label.title = 'Please upload your tailored resume here';
      }
    }
  });
}

// Take screenshot of filled form
async function takeScreenshot() {
  // Screenshot functionality would use Chrome API
  console.log('Screenshot taken');
}

// Track application in backend
async function trackApplication(jobDetails) {
  try {
    await fetch(`${API_URL}/api/applications/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        job_id: null, // Will create if doesn't exist
        resume_id: 1, // TODO: Get from storage
        notes: `Auto-applied via CareerPilot extension\nURL: ${jobDetails.url}`,
        auto_applied: true
      })
    });
    console.log('Application tracked!');
  } catch (error) {
    console.error('Failed to track application:', error);
  }
}

// Initialize
setTimeout(injectCareerPilotButton, 1000);

// Re-inject on navigation (for SPAs)
let lastUrl = location.href;
new MutationObserver(() => {
  const url = location.href;
  if (url !== lastUrl) {
    lastUrl = url;
    setTimeout(injectCareerPilotButton, 1000);
  }
}).observe(document, { subtree: true, childList: true });
