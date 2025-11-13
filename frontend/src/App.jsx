import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import ContentGenerator from './pages/ContentGenerator'
import Scheduling from './pages/Scheduling'
import Analytics from './pages/Analytics'
import RAG from './pages/RAG'
import Settings from './pages/Settings'

function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/content" element={<ContentGenerator />} />
          <Route path="/scheduling" element={<Scheduling />} />
          <Route path="/analytics" element={<Analytics />} />
          <Route path="/rag" element={<RAG />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </Layout>
      <Toaster position="top-right" />
    </Router>
  )
}

export default App

