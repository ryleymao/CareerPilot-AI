import React, { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import {
  BriefcaseIcon,
  DocumentTextIcon,
  CheckCircleIcon,
  ClockIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import axios from 'axios'

export default function Dashboard() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [topMatches, setTopMatches] = useState([])

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [resumeRes, applicationsRes, jobsRes] = await Promise.all([
        axios.get('/api/resumes/'),
        axios.get('/api/applications/'),
        axios.get('/api/jobs/')
      ])

      const resumes = resumeRes.data
      const applications = applicationsRes.data
      const jobs = jobsRes.data.jobs || []

      setStats({
        resumeUploaded: resumes.length > 0,
        totalApplications: applications.length,
        pendingApplications: applications.filter(a => a.status === 'submitted').length,
        totalJobs: jobs.length,
      })

      // Get top 5 matches if resume exists
      if (resumes.length > 0) {
        const matchRes = await axios.get(`/api/matching/matches/${resumes[0].id}?min_score=70&limit=5`)
        setTopMatches(matchRes.data.matches || [])
      }

      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-96">
        <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500"></div>
      </div>
    )
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Dashboard</h1>
        <p className="text-lg text-gray-600">Welcome back! Here's your job search overview</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="card bg-gradient-to-br from-blue-50 to-blue-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Resume Status</p>
              <p className="text-3xl font-bold text-gray-900">
                {stats?.resumeUploaded ? 'Active' : 'Not Uploaded'}
              </p>
            </div>
            <DocumentTextIcon className="w-12 h-12 text-blue-500" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-green-50 to-green-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Applications</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.totalApplications || 0}</p>
            </div>
            <CheckCircleIcon className="w-12 h-12 text-green-500" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-yellow-50 to-yellow-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Pending</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.pendingApplications || 0}</p>
            </div>
            <ClockIcon className="w-12 h-12 text-yellow-500" />
          </div>
        </div>

        <div className="card bg-gradient-to-br from-purple-50 to-purple-100">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600 mb-1">Available Jobs</p>
              <p className="text-3xl font-bold text-gray-900">{stats?.totalJobs || 0}</p>
            </div>
            <BriefcaseIcon className="w-12 h-12 text-purple-500" />
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      {!stats?.resumeUploaded && (
        <div className="card bg-gradient-to-r from-primary-500 to-secondary-500 text-white mb-8">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold mb-2">Get Started!</h2>
              <p className="text-primary-100 mb-4">Upload your resume to start finding perfect job matches</p>
              <Link to="/resume" className="inline-block bg-white text-primary-600 px-6 py-3 rounded-lg font-semibold hover:bg-primary-50 transition">
                Upload Resume Now
              </Link>
            </div>
            <DocumentTextIcon className="w-24 h-24 text-primary-200" />
          </div>
        </div>
      )}

      {/* Top Matches */}
      {topMatches.length > 0 && (
        <div className="card mb-8">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">Top Job Matches</h2>
            <Link to="/jobs" className="text-primary-600 font-semibold hover:text-primary-700">
              View All →
            </Link>
          </div>

          <div className="space-y-4">
            {topMatches.map((match, idx) => (
              <div
                key={idx}
                className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
              >
                <div className="flex-1">
                  <h3 className="font-semibold text-lg">{match.job?.title || 'Job Title'}</h3>
                  <p className="text-gray-600">{match.job?.company || 'Company'}</p>
                  <p className="text-sm text-gray-500 mt-1">
                    {match.job?.location || 'Location'} • {match.job?.job_type || 'Full-time'}
                  </p>
                </div>
                <div className="flex items-center gap-4">
                  <div className="text-right">
                    <div className="text-3xl font-bold text-primary-600">
                      {Math.round(match.overall_score || 0)}%
                    </div>
                    <div className="text-sm text-gray-500">Match</div>
                  </div>
                  <ChartBarIcon className="w-8 h-8 text-gray-400" />
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="card">
          <h2 className="text-2xl font-bold mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <Link
              to="/resume"
              className="block p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition"
            >
              <div className="flex items-center gap-3">
                <DocumentTextIcon className="w-6 h-6 text-primary-600" />
                <div>
                  <p className="font-semibold text-gray-900">Upload Resume</p>
                  <p className="text-sm text-gray-600">Add or update your resume</p>
                </div>
              </div>
            </Link>
            <Link
              to="/jobs"
              className="block p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition"
            >
              <div className="flex items-center gap-3">
                <BriefcaseIcon className="w-6 h-6 text-primary-600" />
                <div>
                  <p className="font-semibold text-gray-900">Browse Jobs</p>
                  <p className="text-sm text-gray-600">Find jobs matching your profile</p>
                </div>
              </div>
            </Link>
            <Link
              to="/applications"
              className="block p-4 bg-primary-50 rounded-lg hover:bg-primary-100 transition"
            >
              <div className="flex items-center gap-3">
                <CheckCircleIcon className="w-6 h-6 text-primary-600" />
                <div>
                  <p className="font-semibold text-gray-900">Track Applications</p>
                  <p className="text-sm text-gray-600">Manage your job applications</p>
                </div>
              </div>
            </Link>
          </div>
        </div>

        <div className="card">
          <h2 className="text-2xl font-bold mb-4">Tips for Success</h2>
          <div className="space-y-4">
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-green-100 text-green-600 rounded-full flex items-center justify-center font-bold">
                1
              </div>
              <div>
                <p className="font-semibold">Focus on high matches</p>
                <p className="text-sm text-gray-600">Apply to jobs with 75%+ match score for better chances</p>
              </div>
            </div>
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-blue-100 text-blue-600 rounded-full flex items-center justify-center font-bold">
                2
              </div>
              <div>
                <p className="font-semibold">Use the Chrome extension</p>
                <p className="text-sm text-gray-600">See match scores on any job site and auto-fill applications</p>
              </div>
            </div>
            <div className="flex gap-3">
              <div className="flex-shrink-0 w-8 h-8 bg-purple-100 text-purple-600 rounded-full flex items-center justify-center font-bold">
                3
              </div>
              <div>
                <p className="font-semibold">Tailor your resume</p>
                <p className="text-sm text-gray-600">Let AI customize your resume for each application</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
