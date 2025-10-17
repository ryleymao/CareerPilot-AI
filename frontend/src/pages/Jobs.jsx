import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { MagnifyingGlassIcon, FunnelIcon, BriefcaseIcon, MapPinIcon, CurrencyDollarIcon, ClockIcon } from '@heroicons/react/24/outline'

export default function Jobs() {
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [searchTerm, setSearchTerm] = useState('')
  const [minScore, setMinScore] = useState(0)
  const [scraping, setScraping] = useState(false)

  useEffect(() => {
    fetchJobs()
  }, [minScore])

  const fetchJobs = async () => {
    try {
      setLoading(true)
      // Get resume first
      const resumeRes = await axios.get('/api/resumes/')
      if (resumeRes.data.length === 0) {
        setLoading(false)
        return
      }

      const resumeId = resumeRes.data[0].id

      // Get matched jobs
      const response = await axios.get(`/api/matching/matches/${resumeId}?min_score=${minScore}&limit=50`)
      setJobs(response.data.matches || [])
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch jobs:', error)
      setLoading(false)
    }
  }

  const handleScrapeJobs = async () => {
    if (!searchTerm) {
      alert('Please enter a job title to search')
      return
    }

    setScraping(true)
    try {
      // Use AI discovery endpoint for better results
      const response = await axios.post('/api/jobs/discover', {
        search_term: searchTerm,
        location: 'Remote',
        results_wanted: 50
      })
      alert(`🤖 AI found ${response.data.jobs_found} fresh, high-quality jobs! Refreshing...`)
      await fetchJobs()
    } catch (error) {
      alert('Failed to find jobs: ' + (error.response?.data?.detail || error.message))
    } finally {
      setScraping(false)
    }
  }

  const filteredJobs = jobs.filter(match =>
    match.job?.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    match.job?.company?.toLowerCase().includes(searchTerm.toLowerCase())
  )

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Job Matches</h1>
        <p className="text-lg text-gray-600">Browse jobs tailored to your profile</p>
      </div>

      {/* Search & Filters */}
      <div className="card mb-8">
        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1 relative">
            <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search by job title or company..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border-2 border-gray-200 rounded-lg focus:border-primary-500 focus:outline-none"
            />
          </div>
          <div className="flex gap-2">
            <select
              value={minScore}
              onChange={(e) => setMinScore(Number(e.target.value))}
              className="px-4 py-3 border-2 border-gray-200 rounded-lg focus:border-primary-500 focus:outline-none"
            >
              <option value={0}>All Matches</option>
              <option value={50}>50%+ Match</option>
              <option value={70}>70%+ Match</option>
              <option value={80}>80%+ Match</option>
            </select>
            <button
              onClick={handleScrapeJobs}
              disabled={scraping}
              className="btn-primary whitespace-nowrap"
            >
              {scraping ? '🤖 AI Searching...' : '🤖 AI Discover Jobs'}
            </button>
          </div>
        </div>
      </div>

      {/* Jobs List */}
      {loading ? (
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500"></div>
        </div>
      ) : filteredJobs.length === 0 ? (
        <div className="card text-center py-16">
          <BriefcaseIcon className="w-20 h-20 mx-auto text-gray-300 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No jobs found</h3>
          <p className="text-gray-500 mb-6">Try adjusting your filters or scrape new jobs</p>
          <button onClick={() => setMinScore(0)} className="btn-secondary">
            Clear Filters
          </button>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredJobs.map((match, idx) => (
            <div key={idx} className="card hover:shadow-xl transition-all duration-200">
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-bold text-gray-900">{match.job?.title || 'Job Title'}</h3>
                    <span className={`px-3 py-1 rounded-full text-sm font-semibold ${
                      (match.overall_score || 0) >= 75 ? 'bg-green-100 text-green-700' :
                      (match.overall_score || 0) >= 50 ? 'bg-yellow-100 text-yellow-700' :
                      'bg-red-100 text-red-700'
                    }`}>
                      {Math.round(match.overall_score || 0)}% Match
                    </span>
                  </div>

                  <p className="text-lg font-semibold text-gray-700 mb-3">{match.job?.company || 'Company'}</p>

                  <div className="flex flex-wrap gap-4 text-sm text-gray-600 mb-4">
                    {match.job?.location && (
                      <div className="flex items-center gap-1">
                        <MapPinIcon className="w-4 h-4" />
                        {match.job.location}
                      </div>
                    )}
                    {match.job?.job_type && (
                      <div className="flex items-center gap-1">
                        <BriefcaseIcon className="w-4 h-4" />
                        {match.job.job_type}
                      </div>
                    )}
                    {match.job?.salary_min && (
                      <div className="flex items-center gap-1">
                        <CurrencyDollarIcon className="w-4 h-4" />
                        ${match.job.salary_min.toLocaleString()} - ${match.job.salary_max?.toLocaleString()}
                      </div>
                    )}
                    {match.job?.posted_date && (
                      <div className="flex items-center gap-1">
                        <ClockIcon className="w-4 h-4" />
                        {new Date(match.job.posted_date).toLocaleDateString()}
                      </div>
                    )}
                  </div>

                  {match.matched_skills && match.matched_skills.length > 0 && (
                    <div className="mb-3">
                      <p className="text-sm font-semibold text-gray-700 mb-2">Matched Skills:</p>
                      <div className="flex flex-wrap gap-2">
                        {match.matched_skills.slice(0, 5).map((skill, sidx) => (
                          <span key={sidx} className="px-2 py-1 bg-green-100 text-green-700 rounded text-xs">
                            {skill}
                          </span>
                        ))}
                        {match.matched_skills.length > 5 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                            +{match.matched_skills.length - 5} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {match.missing_skills && match.missing_skills.length > 0 && (
                    <div>
                      <p className="text-sm font-semibold text-gray-700 mb-2">Missing Skills:</p>
                      <div className="flex flex-wrap gap-2">
                        {match.missing_skills.slice(0, 3).map((skill, sidx) => (
                          <span key={sidx} className="px-2 py-1 bg-red-100 text-red-700 rounded text-xs">
                            {skill}
                          </span>
                        ))}
                        {match.missing_skills.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                            +{match.missing_skills.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                <div className="flex flex-col gap-2 ml-4">
                  {match.job?.url && (
                    <a
                      href={match.job.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition text-center whitespace-nowrap"
                    >
                      View Job
                    </a>
                  )}
                  <button className="px-4 py-2 border-2 border-primary-500 text-primary-600 rounded-lg hover:bg-primary-50 transition whitespace-nowrap">
                    Generate Resume
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
