import React, { useState, useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { CloudArrowUpIcon, DocumentTextIcon, CheckCircleIcon } from '@heroicons/react/24/outline'
import axios from 'axios'

export default function ResumeUpload() {
  const [uploading, setUploading] = useState(false)
  const [uploaded, setUploaded] = useState(false)
  const [resumeData, setResumeData] = useState(null)
  const [error, setError] = useState(null)

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return

    setUploading(true)
    setError(null)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await axios.post('/api/resumes/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      setResumeData(response.data)
      setUploaded(true)
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to upload resume')
    } finally {
      setUploading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    },
    maxFiles: 1
  })

  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Upload Your Resume</h1>
        <p className="text-lg text-gray-600">
          Let AI analyze your experience, skills, and qualifications
        </p>
      </div>

      {/* Dropzone */}
      {!uploaded ? (
        <div
          {...getRootProps()}
          className={`card border-4 border-dashed transition-all duration-200 cursor-pointer ${
            isDragActive
              ? 'border-primary-500 bg-primary-50 scale-105'
              : 'border-gray-300 hover:border-primary-400 hover:bg-primary-25'
          }`}
        >
          <input {...getInputProps()} />
          <div className="text-center py-16">
            <CloudArrowUpIcon className="w-20 h-20 mx-auto text-primary-500 mb-4" />
            {uploading ? (
              <>
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
                <p className="text-xl font-semibold text-gray-700">Analyzing your resume...</p>
                <p className="text-gray-500 mt-2">This may take a few seconds</p>
              </>
            ) : (
              <>
                <p className="text-xl font-semibold text-gray-700 mb-2">
                  {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
                </p>
                <p className="text-gray-500 mb-4">or click to browse</p>
                <p className="text-sm text-gray-400">Supports PDF, DOC, DOCX</p>
              </>
            )}
          </div>
        </div>
      ) : (
        <div className="card bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-200">
          <div className="text-center py-8">
            <CheckCircleIcon className="w-20 h-20 mx-auto text-green-500 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-2">Resume Uploaded Successfully!</h2>
            <p className="text-gray-600 mb-6">AI has analyzed your resume and extracted key information</p>

            {resumeData && (
              <div className="mt-8 grid grid-cols-2 gap-6 text-left">
                <div className="bg-white rounded-lg p-6 shadow">
                  <h3 className="font-semibold text-gray-700 mb-2">Experience</h3>
                  <p className="text-3xl font-bold text-primary-600">
                    {resumeData.experience_years || 0} years
                  </p>
                </div>
                <div className="bg-white rounded-lg p-6 shadow">
                  <h3 className="font-semibold text-gray-700 mb-2">Skills Detected</h3>
                  <p className="text-3xl font-bold text-primary-600">
                    {resumeData.parsed_data?.skills?.length || 0}
                  </p>
                </div>
              </div>
            )}

            <div className="mt-8 space-y-4">
              <button
                onClick={() => setUploaded(false)}
                className="btn-secondary"
              >
                Upload Different Resume
              </button>
            </div>
          </div>
        </div>
      )}

      {error && (
        <div className="mt-4 p-4 bg-red-50 border-l-4 border-red-500 text-red-700">
          <p className="font-semibold">Error</p>
          <p>{error}</p>
        </div>
      )}

      {/* Resume Preview */}
      {resumeData && uploaded && (
        <div className="mt-8 card">
          <h2 className="text-2xl font-bold mb-6">Extracted Information</h2>

          <div className="space-y-6">
            {resumeData.parsed_data?.name && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Name</h3>
                <p className="text-lg">{resumeData.parsed_data.name}</p>
              </div>
            )}

            {resumeData.parsed_data?.email && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Email</h3>
                <p className="text-lg">{resumeData.parsed_data.email}</p>
              </div>
            )}

            {resumeData.parsed_data?.phone && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Phone</h3>
                <p className="text-lg">{resumeData.parsed_data.phone}</p>
              </div>
            )}

            {resumeData.parsed_data?.skills && resumeData.parsed_data.skills.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Skills</h3>
                <div className="flex flex-wrap gap-2">
                  {resumeData.parsed_data.skills.map((skill, idx) => (
                    <span
                      key={idx}
                      className="px-3 py-1 bg-primary-100 text-primary-700 rounded-full text-sm font-medium"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}

            {resumeData.parsed_data?.education && resumeData.parsed_data.education.length > 0 && (
              <div>
                <h3 className="font-semibold text-gray-700 mb-2">Education</h3>
                {resumeData.parsed_data.education.map((edu, idx) => (
                  <div key={idx} className="mb-2">
                    <p className="font-medium">{edu.degree || 'Degree'}</p>
                    <p className="text-gray-600">{edu.institution || ''}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
