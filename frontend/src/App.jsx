import { useState } from 'react'
import Chat from './components/Chat'
import CodebaseMap from './components/CodebaseMap'
import SecurityPanel from './components/SecurityPanel'
import MigrationPanel from './components/MigrationPanel'
import './App.css'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="brand">
  <div className="brand-icon">F</div>
  <div>
    <h1>ForgeBridge</h1>
    <p>Legacy System Intelligence Platform</p>
  </div>
</div>

        <div className="system-info">
          <span className="status-dot"></span>
          AUTOFACTORY-2005
        </div>
      </header>

      {/* Navigation */}
      <nav className="navbar">
  <button
    className={activePage === 'Dashboard' ? 'active' : ''}
    onClick={() => setActivePage('Dashboard')}
  >
    Dashboard
  </button>

  <button
    className={activePage === 'Chat' ? 'active' : ''}
    onClick={() => setActivePage('Chat')}
  >
    Chat
  </button>

  <button
    className={activePage === 'Codebase Map' ? 'active' : ''}
    onClick={() => setActivePage('Codebase Map')}
  >
    Codebase Map
  </button>

  <button
    className={activePage === 'Security' ? 'active' : ''}
    onClick={() => setActivePage('Security')}
  >
    Security
  </button>

  <button
    className={activePage === 'Migration' ? 'active' : ''}
    onClick={() => setActivePage('Migration')}
  >
    Migration
  </button>
</nav>

      {/* Main content */}
      <main className="main">
        {activePage === 'Chat' ? (
  <Chat />
) : activePage === 'Codebase Map' ? (
  <CodebaseMap />
) : activePage === 'Security' ? (
  <SecurityPanel />
) : activePage === 'Migration' ? (
  <MigrationPanel />
) : (
      <div>
        <h2>System Overview</h2>
        <p className="subtitle">
          Monitor and understand the AUTOFACTORY-2005 legacy system.
        </p>

        <div className="cards">

          {/* Test Status */}
          <div className="card">
            <h3>Test Status</h3>
            <div className="card-value success">✓ PASS</div>
            <p>System tests completed successfully</p>
          </div>

          {/* Security */}
          <div className="card">
            <h3>Security Scan</h3>
            <div className="card-value success">✓ SCANNED</div>
            <p>Legacy code security analysis</p>
          </div>

          {/* API */}
          <div className="card">
            <h3>Modernization API</h3>
            <div className="card-value">🔒 READ-ONLY</div>
            <p>No machine control endpoints exposed</p>
          </div>

        </div>

        {/* Machine 7 */}
        <section className="machine-section">
          <h2>Machine 7</h2>

          <div className="machine-status">
            <div>
              <span className="label">Temperature</span>
              <strong>86.2°C</strong>
            </div>

            <div>
              <span className="label">Limit</span>
              <strong>85°C</strong>
            </div>

            <div>
              <span className="label">Production</span>
              <strong className="danger">DISABLED</strong>
            </div>
          </div>

          <div className="alert">
            <strong>⚠ Temperature limit exceeded</strong>
            <p>
              Machine 7 reached 86.2°C, exceeding the configured
              85°C limit. The alarm is active and production is disabled.
            </p>
          </div>
        </section>
      </div>
                )}
      </main>
    </div>
  )
}

export default App