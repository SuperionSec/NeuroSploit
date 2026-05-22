import { Routes, Route } from 'react-router-dom'
import Layout from './components/layout/Layout'
import HomePage from './pages/HomePage'
import NewScanPage from './pages/NewScanPage'
import ScanDetailsPage from './pages/ScanDetailsPage'
import AgentStatusPage from './pages/AgentStatusPage'
import TaskLibraryPage from './pages/TaskLibraryPage'
import RealtimeTaskPage from './pages/RealtimeTaskPage'
import ReportsPage from './pages/ReportsPage'
import ReportViewPage from './pages/ReportViewPage'
import SettingsPage from './pages/SettingsPage'
import SchedulerPage from './pages/SchedulerPage'
import AutoPentestPage from './pages/AutoPentestPage'
import VulnLabPage from './pages/VulnLabPage'
import TerminalAgentPage from './pages/TerminalAgentPage'
import SandboxDashboardPage from './pages/SandboxDashboardPage'
import KnowledgePage from './pages/KnowledgePage'
import MCPManagementPage from './pages/MCPManagementPage'
import ProvidersPage from './pages/ProvidersPage'
import FullIATestingPage from './pages/FullIATestingPage'

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<HomePage />} />
        <Route path="dashboard" element={<HomePage />} />
        <Route path="scan/new" element={<NewScanPage />} />
        <Route path="scan/:scanId" element={<ScanDetailsPage />} />
        <Route path="auto-pentest" element={<AutoPentestPage />} />
        <Route path="full-ia" element={<FullIATestingPage />} />
        <Route path="agent/:agentId" element={<AgentStatusPage />} />
        <Route path="agent" element={<AgentStatusPage />} />
        <Route path="tasks" element={<TaskLibraryPage />} />
        <Route path="realtime" element={<RealtimeTaskPage />} />
        <Route path="reports" element={<ReportsPage />} />
        <Route path="reports/:reportId" element={<ReportViewPage />} />
        <Route path="scheduler" element={<SchedulerPage />} />
        <Route path="vuln-lab" element={<VulnLabPage />} />
        <Route path="terminal" element={<TerminalAgentPage />} />
        <Route path="sandbox" element={<SandboxDashboardPage />} />
        <Route path="knowledge" element={<KnowledgePage />} />
        <Route path="mcp" element={<MCPManagementPage />} />
        <Route path="providers" element={<ProvidersPage />} />
        <Route path="settings" element={<SettingsPage />} />
      </Route>
    </Routes>
  )
}

export default App
