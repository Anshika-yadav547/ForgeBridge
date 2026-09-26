function SecurityPanel() {
  const findings = [
    {
      severity: 'HIGH',
      rule: 'unsafe-memory-operation',
      file: 'legacy/alarm.c',
      line: 42,
      description: 'Potential unsafe memory operation detected.'
    },
    {
      severity: 'MEDIUM',
      rule: 'unchecked-input',
      file: 'legacy/temperature.c',
      line: 28,
      description: 'Input value is not explicitly validated.'
    },
    {
      severity: 'LOW',
      rule: 'deprecated-function',
      file: 'legacy/diagnostics.c',
      line: 15,
      description: 'Deprecated function detected.'
    }
  ]

  return (
    <div className="security-page">

      <h2>Security Analysis</h2>

      <p className="subtitle">
        Security findings detected in the AUTOFACTORY-2005 legacy code.
      </p>

      <div className="security-summary">

        <div className="security-card">
          <span>Total Findings</span>
          <strong>{findings.length}</strong>
        </div>

        <div className="security-card">
          <span>High Severity</span>
          <strong className="high">
            {findings.filter((item) => item.severity === 'HIGH').length}
          </strong>
        </div>

        <div className="security-card">
          <span>Scan Status</span>
          <strong className="success">
            ✓ COMPLETE
          </strong>
        </div>

      </div>

      <div className="findings">

        <h3>Security Findings</h3>

        {findings.map((finding, index) => (
          <div className="finding" key={index}>

            <div className={`severity ${finding.severity.toLowerCase()}`}>
              {finding.severity}
            </div>

            <div className="finding-info">
              <strong>{finding.rule}</strong>

              <span>
                {finding.file}:{finding.line}
              </span>

              <p>{finding.description}</p>
            </div>

          </div>
        ))}

      </div>

    </div>
  )
}

export default SecurityPanel