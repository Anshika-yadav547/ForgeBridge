function MigrationPanel() {
  return (
    <div className="migration-page">
      <h2>Migration & Modernization</h2>

      <p className="subtitle">
        Review the modernization status of the AUTOFACTORY-2005 legacy system.
      </p>

      <div className="migration-summary">

        <div className="migration-card">
          <span>Source System</span>
          <strong>AUTOFACTORY-2005</strong>
          <p>Legacy C system</p>
        </div>

        <div className="migration-card">
          <span>Target Architecture</span>
          <strong>Modern Service</strong>
          <p>Migration plan available</p>
        </div>

        <div className="migration-card">
          <span>Migration Status</span>
          <strong className="status-planned">PLANNED</strong>
          <p>Review required before execution</p>
        </div>

      </div>

      <div className="migration-section">

        <h3>Modernization Plan</h3>

        <div className="migration-step">
          <div className="step-number">1</div>
          <div>
            <strong>Analyze Legacy Code</strong>
            <p>
              Understand modules, dependencies, configuration and
              machine-related logic.
            </p>
          </div>
        </div>

        <div className="migration-step">
          <div className="step-number">2</div>
          <div>
            <strong>Identify Dependencies</strong>
            <p>
              Map relationships between source files, functions and
              configuration files.
            </p>
          </div>
        </div>

        <div className="migration-step">
          <div className="step-number">3</div>
          <div>
            <strong>Prepare Modernization</strong>
            <p>
              Generate a modernization plan while keeping machine
              control interfaces read-only.
            </p>
          </div>
        </div>

        <div className="migration-step">
          <div className="step-number">4</div>
          <div>
            <strong>Review Before Migration</strong>
            <p>
              Review generated changes before any migration is performed.
            </p>
          </div>
        </div>

      </div>

      <div className="read-only-notice">
        <strong>🔒 Read-only modernization interface</strong>
        <p>
          This interface does not directly control or modify the physical
          machine.
        </p>
      </div>

    </div>
  )
}

export default MigrationPanel