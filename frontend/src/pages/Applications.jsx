import React, { useState, useEffect } from 'react'
import axios from 'axios'
import { CheckCircleIcon, ClockIcon, XCircleIcon, EyeIcon } from '@heroicons/react/24/outline'

const STATUS_COLORS = {
  submitted: 'bg-blue-100 text-blue-700',
  interview: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
  offered: 'bg-purple-100 text-purple-700',
  accepted: 'bg-green-100 text-green-700',
  interested: 'bg-yellow-100 text-yellow-700',
  viewed: 'bg-gray-100 text-gray-700'
}

const STATUS_ICONS = {
  submitted: ClockIcon,
  interview: CheckCircleIcon,
  rejected: XCircleIcon,
  offered: CheckCircleIcon,
  accepted: CheckCircleIcon,
  interested: EyeIcon,
  viewed: EyeIcon
}

export default function Applications() {
  const [applications, setApplications] = useState([])
  const [loading, setLoading] = useState(true)
  const [filterStatus, setFilterStatus] = useState('all')

  useEffect(() => {
    fetchApplications()
  }, [])

  const fetchApplications = async () => {
    try {
      const response = await axios.get('/api/applications/')
      setApplications(response.data)
      setLoading(false)
    } catch (error) {
      console.error('Failed to fetch applications:', error)
      setLoading(false)
    }
  }

  const updateStatus = async (appId, newStatus) => {
    try {
      await axios.patch(`/api/applications/${appId}`, { status: newStatus })
      await fetchApplications()
    } catch (error) {
      alert('Failed to update status')
    }
  }

  const filteredApplications = filterStatus === 'all'
    ? applications
    : applications.filter(app => app.status === filterStatus)

  const stats = {
    total: applications.length,
    submitted: applications.filter(a => a.status === 'submitted').length,
    interview: applications.filter(a => a.status === 'interview').length,
    rejected: applications.filter(a => a.status === 'rejected').length,
    offered: applications.filter(a => a.status === 'offered').length
  }

  return (
    <div className="max-w-7xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Application Tracker</h1>
        <p className="text-lg text-gray-600">Manage and track all your job applications</p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
        <div className="card text-center">
          <p className="text-3xl font-bold text-gray-900">{stats.total}</p>
          <p className="text-sm text-gray-600">Total</p>
        </div>
        <div className="card text-center bg-blue-50">
          <p className="text-3xl font-bold text-blue-600">{stats.submitted}</p>
          <p className="text-sm text-gray-600">Submitted</p>
        </div>
        <div className="card text-center bg-green-50">
          <p className="text-3xl font-bold text-green-600">{stats.interview}</p>
          <p className="text-sm text-gray-600">Interviews</p>
        </div>
        <div className="card text-center bg-purple-50">
          <p className="text-3xl font-bold text-purple-600">{stats.offered}</p>
          <p className="text-sm text-gray-600">Offers</p>
        </div>
        <div className="card text-center bg-red-50">
          <p className="text-3xl font-bold text-red-600">{stats.rejected}</p>
          <p className="text-sm text-gray-600">Rejected</p>
        </div>
      </div>

      {/* Filter */}
      <div className="card mb-8">
        <div className="flex gap-2 flex-wrap">
          {['all', 'submitted', 'interview', 'offered', 'rejected', 'interested'].map(status => (
            <button
              key={status}
              onClick={() => setFilterStatus(status)}
              className={`px-4 py-2 rounded-lg font-medium transition ${
                filterStatus === status
                  ? 'bg-primary-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {status.charAt(0).toUpperCase() + status.slice(1)}
            </button>
          ))}
        </div>
      </div>

      {/* Applications List */}
      {loading ? (
        <div className="flex items-center justify-center h-96">
          <div className="animate-spin rounded-full h-16 w-16 border-b-2 border-primary-500"></div>
        </div>
      ) : filteredApplications.length === 0 ? (
        <div className="card text-center py-16">
          <CheckCircleIcon className="w-20 h-20 mx-auto text-gray-300 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No applications yet</h3>
          <p className="text-gray-500">Start applying to jobs to track them here</p>
        </div>
      ) : (
        <div className="space-y-4">
          {filteredApplications.map((app) => {
            const StatusIcon = STATUS_ICONS[app.status] || ClockIcon
            return (
              <div key={app.id} className="card hover:shadow-xl transition-all">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center gap-3 mb-2">
                      <StatusIcon className="w-5 h-5 text-gray-500" />
                      <h3 className="text-xl font-bold text-gray-900">
                        {app.job?.title || 'Application'}
                      </h3>
                      <span className={`px-3 py-1 rounded-full text-sm font-semibold ${STATUS_COLORS[app.status]}`}>
                        {app.status}
                      </span>
                    </div>

                    {app.job?.company && (
                      <p className="text-lg font-semibold text-gray-700 mb-2">{app.job.company}</p>
                    )}

                    <div className="flex gap-4 text-sm text-gray-600 mb-3">
                      <span>Applied: {new Date(app.applied_date).toLocaleDateString()}</span>
                      {app.auto_applied && (
                        <span className="px-2 py-1 bg-blue-100 text-blue-700 rounded">Auto-applied</span>
                      )}
                    </div>

                    {app.notes && (
                      <p className="text-sm text-gray-600 mb-3">{app.notes}</p>
                    )}

                    {/* Status update dropdown */}
                    <div className="flex items-center gap-2">
                      <select
                        value={app.status}
                        onChange={(e) => updateStatus(app.id, e.target.value)}
                        className="px-3 py-2 border border-gray-300 rounded-lg text-sm focus:border-primary-500 focus:outline-none"
                      >
                        <option value="interested">Interested</option>
                        <option value="submitted">Submitted</option>
                        <option value="interview">Interview</option>
                        <option value="offered">Offered</option>
                        <option value="accepted">Accepted</option>
                        <option value="rejected">Rejected</option>
                      </select>
                      <span className="text-sm text-gray-500">Update status</span>
                    </div>
                  </div>

                  {app.job?.url && (
                    <a
                      href={app.job.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition ml-4"
                    >
                      View Job
                    </a>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}
