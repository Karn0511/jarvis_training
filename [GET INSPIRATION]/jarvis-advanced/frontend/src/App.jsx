import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './components/ThemeProvider'
import { Toaster } from './components/ui/toaster'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Chat from './pages/Chat'
import CodeAnalysis from './pages/CodeAnalysis'
import History from './pages/History'
import Settings from './pages/Settings'
import './index.css'

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="jarvis-theme">
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/chat" element={<Chat />} />
            <Route path="/analyze" element={<CodeAnalysis />} />
            <Route path="/history" element={<History />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Layout>
      </Router>
      <Toaster />
    </ThemeProvider>
  )
}

export default App
