import { useState } from 'react'
import { contentAPI, imagesAPI } from '../services/api'
import toast from 'react-hot-toast'
import { Sparkles, Image as ImageIcon, Copy, Check, Wand2, Lightbulb, Zap, Download } from 'lucide-react'

export default function ContentGenerator() {
  const [formData, setFormData] = useState({
    topic: '',
    platform: 'twitter',
    tone: '',
    length: '',
    includeImage: false,
    imageStyle: '',
    brandContext: '',
  })
  const [generatedContent, setGeneratedContent] = useState(null)
  const [generatedImage, setGeneratedImage] = useState(null)
  const [loading, setLoading] = useState(false)
  const [brainstorming, setBrainstorming] = useState(false)
  const [ideas, setIdeas] = useState([])
  const [copied, setCopied] = useState(false)

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      const response = await contentAPI.generate(formData)
      setGeneratedContent(response.data)

      if (formData.includeImage) {
        try {
          const imageResponse = await imagesAPI.generate({
            prompt: formData.topic,
            style: formData.imageStyle,
            width: 512,
            height: 512,
            num_images: 1,
          })
          if (imageResponse.data.image_urls && imageResponse.data.image_urls.length > 0) {
            setGeneratedImage(imageResponse.data.image_urls[0])
          }
        } catch (error) {
          console.error('Image generation failed:', error)
          toast.error('Image generation failed')
        }
      }

      toast.success('Content generated successfully!')
    } catch (error) {
      toast.error('Failed to generate content')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleBrainstorm = async () => {
    setBrainstorming(true)
    try {
      const response = await contentAPI.brainstorm({
        platform: formData.platform,
        count: 5,
      })
      setIdeas(response.data.ideas || [])
      toast.success('Ideas generated successfully!')
    } catch (error) {
      toast.error('Failed to generate ideas')
      console.error(error)
    } finally {
      setBrainstorming(false)
    }
  }

  const handleCopy = () => {
    if (generatedContent) {
      navigator.clipboard.writeText(generatedContent.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
      toast.success('Content copied to clipboard!')
    }
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-purple-600 to-pink-600 bg-clip-text text-transparent mb-2">
            Content Generator
          </h1>
          <p className="text-gray-600">Generate AI-powered social media content with ease</p>
        </div>
        <div className="hidden md:flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-purple-100 to-pink-100 rounded-lg">
          <Wand2 className="h-5 w-5 text-purple-600" />
          <span className="text-sm font-medium text-purple-700">AI Powered</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Form */}
        <div className="glass card-hover rounded-2xl p-8 shadow-xl border border-white/20">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg">
              <Sparkles className="h-6 w-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Generate Content</h2>
          </div>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Topic</label>
              <input
                type="text"
                value={formData.topic}
                onChange={(e) => setFormData({ ...formData, topic: e.target.value })}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="Enter a topic for your content..."
                required
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Platform</label>
              <select
                value={formData.platform}
                onChange={(e) => setFormData({ ...formData, platform: e.target.value })}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all bg-white"
              >
                <option value="twitter">Twitter</option>
                <option value="instagram">Instagram</option>
                <option value="linkedin">LinkedIn</option>
                <option value="facebook">Facebook</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Tone (optional)</label>
              <input
                type="text"
                value={formData.tone}
                onChange={(e) => setFormData({ ...formData, tone: e.target.value })}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                placeholder="Professional, Casual, Funny, etc."
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Brand Context (optional)</label>
              <textarea
                value={formData.brandContext}
                onChange={(e) => setFormData({ ...formData, brandContext: e.target.value })}
                rows={4}
                className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
                placeholder="Brand guidelines, tone of voice, etc."
              />
            </div>

            <div className="flex items-center space-x-3 p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl">
              <input
                type="checkbox"
                id="includeImage"
                checked={formData.includeImage}
                onChange={(e) => setFormData({ ...formData, includeImage: e.target.checked })}
                className="h-5 w-5 text-purple-600 focus:ring-purple-500 rounded"
              />
              <label htmlFor="includeImage" className="flex items-center space-x-2 text-sm font-medium text-gray-700">
                <ImageIcon className="h-4 w-4" />
                <span>Generate image</span>
              </label>
            </div>

            {formData.includeImage && (
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Image Style (optional)</label>
                <input
                  type="text"
                  value={formData.imageStyle}
                  onChange={(e) => setFormData({ ...formData, imageStyle: e.target.value })}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
                  placeholder="Professional, Artistic, Minimalist, etc."
                />
              </div>
            )}

            <div className="flex space-x-4">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 btn-primary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <div className="spinner w-5 h-5 border-2"></div>
                    <span>Generating...</span>
                  </>
                ) : (
                  <>
                    <Zap className="h-5 w-5" />
                    <span>Generate Content</span>
                  </>
                )}
              </button>
              <button
                type="button"
                onClick={handleBrainstorm}
                disabled={brainstorming}
                className="btn-secondary flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Lightbulb className="h-5 w-5" />
                <span>{brainstorming ? 'Thinking...' : 'Brainstorm'}</span>
              </button>
            </div>
          </form>
        </div>

        {/* Results */}
        <div className="space-y-6">
          {generatedContent && (
            <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-gray-900">Generated Content</h2>
                <button
                  onClick={handleCopy}
                  className="p-2 hover:bg-gray-100 rounded-lg transition-colors"
                  title="Copy to clipboard"
                >
                  {copied ? (
                    <Check className="h-5 w-5 text-green-500" />
                  ) : (
                    <Copy className="h-5 w-5 text-gray-600" />
                  )}
                </button>
              </div>
              <div className="prose max-w-none">
                <div className="p-4 bg-gradient-to-r from-purple-50 to-pink-50 rounded-xl border border-purple-100">
                  <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{generatedContent.content}</p>
                </div>
              </div>
              {generatedContent.image_url && (
                <div className="mt-4">
                  <img
                    src={generatedContent.image_url}
                    alt="Generated"
                    className="w-full rounded-xl shadow-lg"
                  />
                </div>
              )}
            </div>
          )}

          {generatedImage && (
            <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Generated Image</h2>
              <img
                src={generatedImage}
                alt="Generated"
                className="w-full rounded-xl shadow-lg"
              />
            </div>
          )}

          {ideas.length > 0 && (
            <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
              <div className="flex items-center space-x-2 mb-4">
                <Lightbulb className="h-6 w-6 text-yellow-500" />
                <h2 className="text-xl font-bold text-gray-900">Content Ideas</h2>
              </div>
              <div className="space-y-4">
                {ideas.map((idea, index) => (
                  <div key={index} className="p-4 bg-gradient-to-r from-yellow-50 to-orange-50 rounded-xl border border-yellow-100">
                    <h3 className="font-bold text-gray-900 mb-2">{idea.title || `Idea ${index + 1}`}</h3>
                    {idea.hook && <p className="text-sm text-gray-700 mb-3">{idea.hook}</p>}
                    {idea.hashtags && (
                      <div className="flex flex-wrap gap-2">
                        {idea.hashtags.map((tag, tagIndex) => (
                          <span key={tagIndex} className="px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 rounded-full text-xs font-semibold">
                            {tag}
                          </span>
                        ))}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}

          {!generatedContent && !generatedImage && ideas.length === 0 && (
            <div className="glass rounded-2xl p-12 text-center border border-white/20">
              <Sparkles className="h-16 w-16 text-purple-400 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-700 mb-2">Ready to Generate</h3>
              <p className="text-gray-500">Fill out the form and click generate to create amazing content!</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
