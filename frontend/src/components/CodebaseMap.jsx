function CodebaseMap() {
  return (
    <div className="codebase-page">
      <h2>Codebase Map</h2>

      <p className="subtitle">
        Explore the structure and dependencies of AUTOFACTORY-2005.
      </p>

      <div className="map-container">

        {/* Connection lines */}
        <svg className="map-lines">
          <line x1="50%" y1="105" x2="25%" y2="190" />
          <line x1="50%" y1="105" x2="75%" y2="190" />
          <line x1="25%" y1="260" x2="35%" y2="390" />
          <line x1="75%" y1="260" x2="65%" y2="390" />
        </svg>

        {/* Main node */}
        <div className="map-node main-node">
          <strong>main.c</strong>
          <span>Entry Point</span>
        </div>

        {/* Second level */}
        <div className="map-node node-1">
          <strong>alarm.c</strong>
          <span>Alarm Logic</span>
        </div>

        <div className="map-node node-2">
          <strong>temperature.c</strong>
          <span>Temperature Monitoring</span>
        </div>

        {/* Third level */}
        <div className="map-node node-3">
          <strong>limits.cfg</strong>
          <span>Temperature Limits</span>
        </div>

        <div className="map-node node-4">
          <strong>diagnostics.c</strong>
          <span>Diagnostics</span>
        </div>

      </div>

      <div className="map-legend">
        <strong>Legend</strong>
        <span>● Source File</span>
        <span>→ Dependency</span>
      </div>
    </div>
  )
}

export default CodebaseMap