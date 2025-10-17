// CareerPilot Background Service Worker
console.log('CareerPilot background service worker loaded');

// Track applications that were opened externally
const externalApplications = new Map();

// Listen for tab updates to detect external application pages
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  if (changeInfo.status === 'complete' && tab.url) {
    // Check if this was an external application link we tracked
    const jobData = externalApplications.get(tabId);

    if (jobData) {
      // Show popup asking if they applied
      setTimeout(() => {
        askIfApplied(tabId, jobData);
      }, 5000); // Wait 5 seconds for them to apply
    }
  }
});

// Track when user clicks on external application links
chrome.webNavigation.onBeforeNavigate.addListener((details) => {
  if (details.frameId === 0) { // Main frame only
    const url = details.url;

    // Detect if it's an external application page
    if (url.includes('apply') || url.includes('application') || url.includes('careers')) {
      // Store this tab for tracking
      chrome.storage.local.get(['currentJob'], (result) => {
        if (result.currentJob) {
          externalApplications.set(details.tabId, result.currentJob);
        }
      });
    }
  }
});

// Ask user if they applied
async function askIfApplied(tabId, jobData) {
  try {
    await chrome.tabs.sendMessage(tabId, {
      action: 'showAppliedPrompt',
      job: jobData
    });
  } catch (error) {
    console.error('Could not show applied prompt:', error);
  }
}

// Handle messages from content scripts
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === 'trackExternalApplication') {
    // Store current job data for tracking
    chrome.storage.local.set({ currentJob: request.job });
    sendResponse({ success: true });
  } else if (request.action === 'userApplied') {
    // Track the application
    trackApplication(request.job, true);
    externalApplications.delete(sender.tab.id);
    sendResponse({ success: true });
  } else if (request.action === 'userDidNotApply') {
    // Clean up tracking
    externalApplications.delete(sender.tab.id);
    sendResponse({ success: true });
  }

  return true;
});

// Track application in backend
async function trackApplication(jobData, applied) {
  const API_URL = 'http://localhost:8000';

  try {
    await fetch(`${API_URL}/api/applications/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        job_id: null,
        resume_id: 1,
        notes: `External application\nURL: ${jobData.url}`,
        status: applied ? 'submitted' : 'viewed',
        auto_applied: false
      })
    });
  } catch (error) {
    console.error('Failed to track application:', error);
  }
}
