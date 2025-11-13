import { useState } from 'react'
import { ragAPI } from '../services/api'
import toast from 'react-hot-toast'
import { Upload, Search, FileText, X, Database, Sparkles, CheckCircle, File } from 'lucide-react'

export default function RAG() {
  const [searchQuery, setSearchQuery] = useState('')
  const [searchResults, setSearchResults] = useState([])
  const [documentContent, setDocumentContent] = useState('')
  const [uploadedFile, setUploadedFile] = useState(null)
  const [loading, setLoading] = useState(false)
  const [searching, setSearching] = useState(false)

  const handleUpload = async (e) => {
    e.preventDefault()
    setLoading(true)

    try {
      if (uploadedFile) {
        await ragAPI.uploadFile(uploadedFile)
        toast.success('File uploaded successfully!')
        setUploadedFile(null)
      } else if (documentContent) {
        await ragAPI.upload({
          content: documentContent,
          metadata: { type: 'text' },
        })
        toast.success('Document uploaded successfully!')
        setDocumentContent('')
      }
    } catch (error) {
      toast.error('Failed to upload document')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = async (e) => {
    e.preventDefault()
    setSearching(true)

    try {
      const response = await ragAPI.search(searchQuery, 5)
      setSearchResults(response.data.results || [])
    } catch (error) {
      toast.error('Failed to search documents')
      console.error(error)
    } finally {
      setSearching(false)
    }
  }

  return (
    <div className="space-y-8 animate-fadeIn">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-2">
            RAG Knowledge Base
          </h1>
          <p className="text-gray-600">Upload and search brand documents, tone guides, and FAQs</p>
        </div>
        <div className="hidden md:flex items-center space-x-2 px-4 py-2 bg-gradient-to-r from-indigo-100 to-purple-100 rounded-lg">
          <Database className="h-5 w-5 text-indigo-600" />
          <span className="text-sm font-medium text-indigo-700">Vector Search</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Upload Section */}
        <div className="space-y-6">
          <div className="glass card-hover rounded-2xl p-8 shadow-xl border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <div className="p-2 bg-gradient-to-r from-indigo-500 to-purple-500 rounded-lg">
                <Upload className="h-6 w-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Upload Document</h2>
            </div>
            
            <form onSubmit={handleUpload} className="space-y-6">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">Document Content</label>
                <textarea
                  value={documentContent}
                  onChange={(e) => setDocumentContent(e.target.value)}
                  rows={6}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all resize-none"
                  placeholder="Paste document content here..."
                />
              </div>

              <div className="relative">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Or Upload File</label>
                <div className="flex items-center justify-center w-full">
                  <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-xl cursor-pointer bg-gray-50 hover:bg-gray-100 transition-colors">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                      <File className="h-10 w-10 text-gray-400 mb-2" />
                      <p className="mb-2 text-sm text-gray-500">
                        <span className="font-semibold">Click to upload</span> or drag and drop
                      </p>
                      <p className="text-xs text-gray-500">PDF, TXT, DOCX (MAX. 10MB)</p>
                    </div>
                    <input
                      type="file"
                      className="hidden"
                      onChange={(e) => setUploadedFile(e.target.files[0])}
                    />
                  </label>
                </div>
                {uploadedFile && (
                  <div className="mt-2 flex items-center space-x-2 text-sm text-gray-600">
                    <File className="h-4 w-4" />
                    <span>{uploadedFile.name}</span>
                    <button
                      onClick={() => setUploadedFile(null)}
                      className="text-red-500 hover:text-red-700"
                    >
                      <X className="h-4 w-4" />
                    </button>
                  </div>
                )}
              </div>

              <button
                type="submit"
                disabled={loading || (!documentContent && !uploadedFile)}
                className="w-full btn-primary bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? (
                  <>
                    <div className="spinner w-5 h-5"></div>
                    <span>Uploading...</span>
                  </>
                ) : (
                  <>
                    <Upload className="h-5 w-5" />
                    <span>Upload Document</span>
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Search Section */}
          <div className="glass card-hover rounded-2xl p-8 shadow-xl border border-white/20">
            <div className="flex items-center space-x-3 mb-6">
              <div className="p-2 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-lg">
                <Search className="h-6 w-6 text-white" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Search Documents</h2>
            </div>
            
            <form onSubmit={handleSearch} className="space-y-4">
              <div>
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-4 py-3 rounded-xl border border-gray-200 focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
                  placeholder="Search for relevant content..."
                />
              </div>

              <button
                type="submit"
                disabled={searching || !searchQuery}
                className="w-full btn-secondary bg-gradient-to-r from-blue-600 to-cyan-600 flex items-center justify-center space-x-2 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {searching ? (
                  <>
                    <div className="spinner w-5 h-5"></div>
                    <span>Searching...</span>
                  </>
                ) : (
                  <>
                    <Search className="h-5 w-5" />
                    <span>Search</span>
                  </>
                )}
              </button>
            </form>
          </div>
        </div>

        {/* Results Section */}
        <div className="glass card-hover rounded-2xl p-6 shadow-xl border border-white/20">
          <div className="flex items-center space-x-3 mb-6">
            <div className="p-2 bg-gradient-to-r from-green-500 to-emerald-500 rounded-lg">
              <FileText className="h-6 w-6 text-white" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Search Results</h2>
          </div>
          
          <div className="space-y-4 max-h-[700px] overflow-y-auto">
            {searchResults.length === 0 ? (
              <div className="text-center py-12">
                <Database className="h-16 w-16 text-gray-300 mx-auto mb-4" />
                <p className="text-gray-500 font-medium mb-2">No results yet</p>
                <p className="text-sm text-gray-400">Search for documents to see results here</p>
              </div>
            ) : (
              searchResults.map((result, index) => (
                <div
                  key={index}
                  className="p-5 bg-gradient-to-r from-white to-gray-50 rounded-xl border border-gray-200 hover:shadow-lg transition-all duration-200"
                >
                  <div className="flex items-start justify-between mb-3">
                    <div className="flex items-center space-x-2">
                      <div className="p-2 bg-gradient-to-r from-blue-100 to-cyan-100 rounded-lg">
                        <FileText className="h-4 w-4 text-blue-600" />
                      </div>
                      <span className="text-xs font-semibold text-gray-600">Result {index + 1}</span>
                    </div>
                    {result.score && (
                      <span className="px-2 py-1 bg-green-100 text-green-700 rounded-full text-xs font-semibold">
                        {(result.score * 100).toFixed(1)}% match
                      </span>
                    )}
                  </div>
                  <p className="text-sm text-gray-700 mb-3 leading-relaxed">{result.content}</p>
                  {result.metadata && (
                    <div className="flex items-center space-x-2 text-xs text-gray-500">
                      <File className="h-3 w-3" />
                      <span>Source: {result.metadata.filename || 'Unknown'}</span>
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
