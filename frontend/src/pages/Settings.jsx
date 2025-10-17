import React from 'react'
import { Cog6ToothIcon } from '@heroicons/react/24/outline'

export default function Settings() {
  return (
    <div className="max-w-4xl mx-auto">
      <div className="mb-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-2">Settings</h1>
        <p className="text-lg text-gray-600">Configure your CareerPilot preferences</p>
      </div>

      <div className="card">
        <div className="text-center py-16">
          <Cog6ToothIcon className="w-20 h-20 mx-auto text-gray-300 mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">Settings Coming Soon</h3>
          <p className="text-gray-500">Configure job preferences, notifications, and more</p>
        </div>
      </div>
    </div>
  )
}
