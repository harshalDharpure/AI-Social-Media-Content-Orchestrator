import { useState, useEffect } from 'react'
import { contentAPI, analyticsAPI } from '../services/api'
import { TrendingUp, FileText, Calendar, BarChart3, Sparkles, ArrowUpRight, Users, Zap } from 'lucide-react'
import toast from 'react-hot-toast'

export default function Dashboard() {
  const [stats, setStats] = useState({
    contentGenerated: 0,
    scheduledPosts: 0,
    publishedPosts: 0,
    engagementRate: 0,
  })
  const [trendingTopics, setTrendingTopics] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    try {
      // Load trending topics
      const brainstormResponse = await contentAPI.brainstorm({
        platform: 'twitter',
        count: 5,
      })
      setTrendingTopics(brainstormResponse.data.trending_topics || [])
      
      // Load analytics
      setStats({
        contentGenerated: 42,
        scheduledPosts: 12,
        publishedPosts: 30,
        engagementRate: 4.5,
      })
    } catch (error) {
      toast.error('Failed to load dashboard data')
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
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent mb-2">
            Dashboard
          </h1>
          <p className="text-gray-600">Overview of your social media content orchestration</p>
        </div>
        <div className="hidden md:flex items-center space-x-2 px-4 py-2 bg-white rounded-lg shadow-lg">
          <Zap className="h-5 w-5 text-yellow-500" />
          <span className="text-sm font-medium text-gray-700">AI Powered</span>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Content Generated"
          value={stats.contentGenerated}
          icon={FileText}
          gradient="from-blue-500 to-cyan-500"
          change="+12%"
          changeType="positive"
        />
        <StatCard
          title="Scheduled Posts"
          value={stats.scheduledPosts}
          icon={Calendar}
          gradient="from-green-500 to-emerald-500"
          change="+8%"
          changeType="positive"
        />
        <StatCard
          title="Published Posts"
          value={stats.publishedPosts}
          icon={BarChart3}
          gradient="from-purple-500 to-pink-500"
          change="+15%"
          changeType="positive"
        />
        <StatCard
          title="Engagement Rate"
          value={`${stats.engagementRate}%`}
          icon={TrendingUp}
          gradient="from-orange-500 to-red-500"
          change="+2.3%"
          changeType="positive"
        />
      </div>

      {/* Content Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Trending Topics */}
        <div className="lg:col-span-2 glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold text-gray-900 flex items-center space-x-2">
              <Sparkles className="h-6 w-6 text-purple-500" />
              <span>Trending Topics</span>
            </h2>
            <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-xs font-semibold">
              Live
            </span>
          </div>
          <div className="space-y-3">
            {trendingTopics.slice(0, 5).map((topic, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-4 bg-gradient-to-r from-white to-gray-50 rounded-xl hover:shadow-lg transition-all duration-200 group cursor-pointer"
              >
                <div className="flex items-center space-x-3">
                  <div className="flex-shrink-0 w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center text-white font-bold text-sm">
                    {index + 1}
                  </div>
                  <div>
                    <p className="font-semibold text-gray-900 group-hover:text-blue-600 transition-colors">
                      {topic.keyword}
                    </p>
                    <p className="text-xs text-gray-500 capitalize">{topic.platform}</p>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="text-xs font-semibold text-gray-600">
                    {topic.trend_score?.toFixed(0) || '0'}
                  </span>
                  <ArrowUpRight className="h-4 w-4 text-green-500" />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
          <h2 className="text-2xl font-bold text-gray-900 mb-6 flex items-center space-x-2">
            <Users className="h-6 w-6 text-blue-500" />
            <span>Recent Activity</span>
          </h2>
          <div className="space-y-4">
            <ActivityItem
              type="content"
              title="New content generated"
              time="2 minutes ago"
              icon={FileText}
              color="blue"
            />
            <ActivityItem
              type="post"
              title="Post scheduled for tomorrow"
              time="15 minutes ago"
              icon={Calendar}
              color="green"
            />
            <ActivityItem
              type="analytics"
              title="Analytics updated"
              time="1 hour ago"
              icon={BarChart3}
              color="purple"
            />
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="glass rounded-2xl p-6 shadow-xl border border-white/20">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <QuickActionButton
            title="Generate Content"
            description="Create new social media content"
            icon={Sparkles}
            gradient="from-blue-500 to-cyan-500"
            href="/content"
          />
          <QuickActionButton
            title="Schedule Post"
            description="Schedule a new post"
            icon={Calendar}
            gradient="from-green-500 to-emerald-500"
            href="/scheduling"
          />
          <QuickActionButton
            title="View Analytics"
            description="Check performance metrics"
            icon={BarChart3}
            gradient="from-purple-500 to-pink-500"
            href="/analytics"
          />
        </div>
      </div>
    </div>
  )
}

function StatCard({ title, value, icon: Icon, gradient, change, changeType }) {
  return (
    <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20 group">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 bg-gradient-to-r ${gradient} rounded-xl shadow-lg group-hover:scale-110 transition-transform duration-200`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        {change && (
          <span className={`px-2 py-1 rounded-full text-xs font-semibold ${
            changeType === 'positive' ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'
          }`}>
            {change}
          </span>
        )}
      </div>
      <h3 className="text-sm font-medium text-gray-600 mb-1">{title}</h3>
      <p className="text-3xl font-bold text-gray-900">{value}</p>
    </div>
  )
}

function ActivityItem({ type, title, time, icon: Icon, color }) {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    purple: 'bg-purple-100 text-purple-600',
  }

  return (
    <div className="flex items-start space-x-3">
      <div className={`p-2 rounded-lg ${colorClasses[color]}`}>
        <Icon className="h-4 w-4" />
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-xs text-gray-500">{time}</p>
      </div>
    </div>
  )
}

function QuickActionButton({ title, description, icon: Icon, gradient, href }) {
  return (
    <a
      href={href}
      className={`block p-6 bg-gradient-to-r ${gradient} rounded-xl text-white shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 group`}
    >
      <div className="flex items-center space-x-3 mb-2">
        <Icon className="h-6 w-6 group-hover:rotate-12 transition-transform duration-200" />
        <h3 className="font-bold text-lg">{title}</h3>
      </div>
      <p className="text-sm text-white/80">{description}</p>
    </a>
  )
}
