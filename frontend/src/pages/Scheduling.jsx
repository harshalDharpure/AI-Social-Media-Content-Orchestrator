import { useState, useEffect } from 'react'
import { schedulingAPI, socialMediaAPI } from '../services/api'
import toast from 'react-hot-toast'
import { Calendar, Clock, CheckCircle, XCircle, Send, Plus, Trash2, Sparkles } from 'lucide-react'

export default function Scheduling() {
  const [scheduledPosts, setScheduledPosts] = useState([])
  const [formData, setFormData] = useState({
    content: '',
    platform: 'twitter',
    content_id: '',
    image_url: '',
    schedule_for: '',
  })
  const [loading, setLoading] = useState(false)
  const [platforms, setPlatforms] = useState([])

  useEffect(() => {
    loadScheduledPosts()
    loadPlatforms()
  }, [])

  const loadScheduledPosts = async () => {
    try {
      const response = await schedulingAPI.getScheduled()
      setScheduledPosts(response.data || [])
    } catch (error) {
      console.error('Failed to load scheduled posts:', error)
    }
  }

  const loadPlatforms = async () => {
    try {
      const response = await socialMediaAPI.getPlatforms()
      setPlatforms(response.data.platforms || [])
    } catch (error) {
      console.error('Failed to load platforms:', error)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const scheduleData = {
        ...formData,
        schedule_for: formData.schedule_for ? new Date(formData.schedule_for).toISOString() : null,
      }

      await schedulingAPI.schedule(scheduleData)
      toast.success('Post scheduled successfully!')
      setFormData({
        content: '',
        platform: 'twitter',
        content_id: '',
        image_url: '',
        schedule_for: '',
      })
      loadScheduledPosts()
    } catch (error) {
      toast.error('Failed to schedule post')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleCancel = async (id) => {
    try {
      await schedulingAPI.cancel(id)
      toast.success('Post cancelled successfully!')
      loadScheduledPosts()
    } catch (error) {
      toast.error('Failed to cancel post')
      console.error(error)
    }
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-green-600 to-emerald-600 bg-clip-text text-transparent mb-2">
            Scheduling
          </h1>
          <p className="text-gray-600">Schedule and manage your social media posts</p>
        </div>
        <div className="hidden md:flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-green-100 to-emerald-100 rounded-lg">
          <Calendar className="h-5 w-5 text-green-600" />
          <span className="text-sm font-medium text-green-700">Auto Schedule</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Schedule Form */}
        <div className="glass card-hover rounded-2xl p-8 shadow-xl border border-white/20">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg">
              <Plus className="h-6 w-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Schedule Post</h2>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Content</label>
              <textarea
                value={formData.content}
                onChange={(e) => setFormData({ ...formData, content: e.target.value })}
                rows={6}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all resize-none"
                placeholder="Enter your post content..."
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Platform</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all bg-white"
              >
                {platforms.map((platform) => (
                  <option key={platform.name} value={platform.name}>
                    {platform.name.charAt(0).toUpperCase() + platform.name.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Image URL (optional)</label>
              <input
                type="url"
                value={formData.image_url}
                onChange={(e) => setFormData({ ...formData, image_url: e.target.value })}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
                placeholder="https://example.com/image.jpg"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Schedule For (leave empty for immediate)</label>
              <input
                type="datetime-local"
                value={formData.schedule_for}
                onChange={(e) => setFormData({ ...formData, schedule_for: e.target.value })}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-green-500 focus:border-transparent transition-all"
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full btn-primary bg-gradient-to-r from-green-600 to-emerald-600 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {loading ? (
                <>
                  <div className="spinner w-5 h-5"></div>
                  <span>Scheduling...</span>
                </>
              ) : (
                <>
                  <Send className="h-5 w-5" />
                  <span>Schedule Post</span>
                </>
              )}
            </button>
          </form>
        </div>

        {/* Scheduled Posts */}
        <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg">
              <Clock className="h-6 w-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Scheduled Posts</h2>
          </div>
          
          <div className="space-y-4 max-h-[600px] overflow-y-auto">
            {scheduledPosts.length === 0 ? (
              <div className="text-center py-12">
                <Calendar className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 font-medium">No scheduled posts</p>
                <p className="text-sm text-gray-400 mt-2">Schedule your first post to get started</p>
              </div>
            ) : (
              scheduledPosts.map((post) => (
                <div key={post.id} className="p-4 bg-gradient-to-r from-white to-gray-50 rounded-xl border border-gray-200 hover:shadow-lg transition-all duration-200">
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <div className="flex items-center space-x-2 mb-2">
                        <span className="px-3 py-1 bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 rounded-full text-xs font-semibold capitalize">
                          {post.platform}
                        </span>
                        {post.status === 'scheduled' && (
                          <span className="flex items-center space-x-1 text-yellow-600">
                            <Clock className="h-4 w-4" />
                            <span className="text-xs font-medium">Scheduled</span>
                          </span>
                        )}
                        {post.status === 'published' && (
                          <span className="flex items-center space-x-1 text-green-600">
                            <CheckCircle className="h-4 w-4" />
                            <span className="text-xs font-medium">Published</span>
                          </span>
                        )}
                        {post.status === 'failed' && (
                          <span className="flex items-center space-x-1 text-red-600">
                            <XCircle className="h-4 w-4" />
                            <span className="text-xs font-medium">Failed</span>
                          </span>
                        )}
                      </div>
                      {post.scheduled_for && (
                        <p className="text-sm text-gray-600 mb-2">
                          <Clock className="h-4 w-4 inline mr-1" />
                          {new Date(post.scheduled_for).toLocaleString()}
                        </p>
                      )}
                    </div>
                    {post.status === 'scheduled' && (
                      <button
                        onClick={() => handleCancel(post.id)}
                        className="p-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
                        title="Cancel post"
                      >
                        <Trash2 className="h-5 w-5" />
                      </button>
                    )}
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
