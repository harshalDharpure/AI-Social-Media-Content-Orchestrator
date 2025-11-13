export default function Settings() {
  return (
    <div className="px-4 py-6 sm:px-0">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="mt-2 text-sm text-gray-600">Configure your AI Social Media Content Orchestrator</p>
      </div>

      <div className="bg-white shadow rounded-lg p-6">
        <h2 className="text-lg font-medium text-gray-900 mb-4">API Configuration</h2>
        <p className="text-sm text-gray-600">
          Configure your API keys in the backend .env file. See the README for more information.
        </p>
      </div>
    </div>
  )
}

