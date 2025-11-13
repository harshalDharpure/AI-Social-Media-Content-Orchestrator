import { useState, useEffect } from 'react'
import { analyticsAPI } from '../services/api'
import toast from 'react-hot-toast'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts'
import { TrendingUp, Eye, Heart, MessageCircle, Share2, BarChart3, Zap, ArrowUpRight, ArrowDownRight } from 'lucide-react'

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#43e97b', '#fa709a']

export default function Analytics() {
  const [analytics, setAnalytics] = useState(null)
  const [platform, setPlatform] = useState('twitter')
  const [days, setDays] = useState(7)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    loadAnalytics()
  }, [platform, days])

  const loadAnalytics = async () => {
    setLoading(true)
    try {
      const response = await analyticsAPI.getPlatformAnalytics(platform, days)
      setAnalytics(response.data)
    } catch (error) {
      toast.error('Failed to load analytics')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh]">
        <div className="text-center">
          <div className="spinner mx-auto mb-4"></div>
          <p className="text-gray-600">Loading analytics...</p>
        </div>
      </div>
    )
  }

  const chartData = analytics?.metrics ? [
    { name: 'Impressions', value: analytics.metrics.impressions },
    { name: 'Engagement', value: analytics.metrics.engagement },
    { name: 'Likes', value: analytics.metrics.likes },
    { name: 'Shares', value: analytics.metrics.shares },
    { name: 'Comments', value: analytics.metrics.comments },
  ] : []

  const pieData = analytics?.metrics ? [
    { name: 'Likes', value: analytics.metrics.likes },
    { name: 'Shares', value: analytics.metrics.shares },
    { name: 'Comments', value: analytics.metrics.comments },
  ] : []

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent mb-2">
            Analytics
          </h1>
          <p className="text-gray-600">Track your social media performance and insights</p>
        </div>
        <div className="hidden md:flex items-center space-x-4">
          <select
            value={platform}
            onChange={(e) => setPlatform(e.target.value)}
            className="px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all bg-white shadow-sm"
          >
            <option value="twitter">Twitter</option>
            <option value="instagram">Instagram</option>
            <option value="linkedin">LinkedIn</option>
          </select>
          <select
            value={days}
            onChange={(e) => setDays(Number(e.target.value))}
            className="px-4 py-2 rounded-xl border border-gray-200 focus:ring-2 focus:ring-orange-500 focus:border-transparent transition-all bg-white shadow-sm"
          >
            <option value={7}>Last 7 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      {analytics && (
        <>
          {/* Metrics Grid */}
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-5">
            <MetricCard
              title="Impressions"
              value={analytics.metrics.impressions}
              icon={Eye}
              gradient="from-blue-500 to-cyan-500"
              change="+12%"
              changeType="positive"
            />
            <MetricCard
              title="Engagement"
              value={analytics.metrics.engagement}
              icon={TrendingUp}
              gradient="from-green-500 to-emerald-500"
              change="+8%"
              changeType="positive"
            />
            <MetricCard
              title="Likes"
              value={analytics.metrics.likes}
              icon={Heart}
              gradient="from-red-500 to-pink-500"
              change="+15%"
              changeType="positive"
            />
            <MetricCard
              title="Comments"
              value={analytics.metrics.comments}
              icon={MessageCircle}
              gradient="from-purple-500 to-indigo-500"
              change="+5%"
              changeType="positive"
            />
            <MetricCard
              title="Shares"
              value={analytics.metrics.shares}
              icon={Share2}
              gradient="from-orange-500 to-yellow-500"
              change="+20%"
              changeType="positive"
            />
          </div>

          {/* Charts */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
              <div className="flex items-center space-x-2 mb-6">
                <BarChart3 className="h-6 w-6 text-blue-500" />
                <h2 className="text-xl font-bold text-gray-900">Metrics Overview</h2>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
                  <XAxis dataKey="name" stroke="#6b7280" />
                  <YAxis stroke="#6b7280" />
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                    }}
                  />
                  <Legend />
                  <Bar dataKey="value" fill="#667eea" radius={[8, 8, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
              <div className="flex items-center space-x-2 mb-6">
                <TrendingUp className="h-6 w-6 text-purple-500" />
                <h2 className="text-xl font-bold text-gray-900">Engagement Distribution</h2>
              </div>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: 'white',
                      border: '1px solid #e5e7eb',
                      borderRadius: '8px',
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Recommendations */}
          {analytics.recommendations && analytics.recommendations.length > 0 && (
            <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
              <div className="flex items-center space-x-2 mb-6">
                <Zap className="h-6 w-6 text-yellow-500" />
                <h2 className="text-xl font-bold text-gray-900">AI Recommendations</h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {analytics.recommendations.map((rec, index) => (
                  <div
                    key={index}
                    className="flex items-start space-x-3 p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl border border-yellow-100"
                  >
                    <div className="flex-shrink-0 w-6 h-6 bg-gradient-to-r from-yellow-400 to-orange-400 rounded-full flex items-center justify-center text-white font-bold text-sm">
                      {index + 1}
                    </div>
                    <p className="text-sm font-medium text-gray-700">{rec}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}

      {!analytics && (
        <div className="glass rounded-2xl p-12 text-center border border-white/20">
          <BarChart3 className="h-16 w-16 text-gray-300 mx-auto mb-4" />
          <h3 className="text-xl font-semibold text-gray-700 mb-2">No Analytics Data</h3>
          <p className="text-gray-500">Analytics data will appear here once you start posting content.</p>
        </div>
      )}
    </div>
  )
}

function MetricCard({ title, value, icon: Icon, gradient, change, changeType }) {
  return (
    <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20 group">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 bg-gradient-to-r ${gradient} rounded-xl shadow-lg group-hover:scale-110 transition-transform duration-200`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        {change && (
          <div className={`flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-semibold ${
            changeType === 'positive' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {changeType === 'positive' ? (
              <ArrowUpRight className="h-3 w-3" />
            ) : (
              <ArrowDownRight className="h-3 w-3" />
            )}
            <span>{change}</span>
          </div>
        )}
      </div>
      <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
      <p className="text-3xl font-bold text-gray-900">{value.toLocaleString()}</p>
    </div>
  )
}
