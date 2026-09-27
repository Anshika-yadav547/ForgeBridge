import { useEffect,useState } from 'react'
import Chat from './components/Chat'
import CodebaseMap from './components/CodebaseMap'
import SecurityPanel from './components/SecurityPanel'
import MigrationPanel from './components/MigrationPanel'
import { getMachineStatus } from './api'
import './App.css'

function App() {
  const [activePage, setActivePage] = useState('Dashboard')
 const [machine, setMachine] = useState(null)
  const [machineError, setMachineError] = useState('')

  useEffect(() => {
    getMachineStatus(7)
      .then((data) => {
        setMachine(data)
      })
      .catch((error) => {
        console.error(error)
        setMachineError('Unable to load machine status')
      })
  }, [])

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

  {machineError ? (
    <div className="alert">
      <strong>⚠ {machineError}</strong>
    </div>
  ) : machine ? (
    <>
      <div className="machine-status">

        <div>
          <span className="label">Temperature</span>
          <strong>{machine.temperature}°C</strong>
        </div>

        <div>
          <span className="label">Limit</span>
          <strong>{machine.limit}°C</strong>
        </div>

        <div>
          <span className="label">Production</span>
          <strong className="danger">
            {machine.production_enabled ? 'ENABLED' : 'DISABLED'}
          </strong>
        </div>

      </div>

      <div className="alert">
        <strong>
          {machine.alarm_active
            ? '⚠ Temperature limit exceeded'
            : '✓ Machine operating normally'}
        </strong>

        <p>{machine.reason}</p>
      </div>
    </>
  ) : (
    <p>Loading machine status...</p>
  )}

</section>
      </div>
                )}
      </main>
    </div>
  )
}

export default App