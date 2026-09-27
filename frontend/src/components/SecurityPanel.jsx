import { useEffect, useState } from 'react'

function SecurityPanel() {
  const [scan, setScan] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/security')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to load security scan')
        }

        return response.json()
      })
      .then((data) => {
        setScan(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="security-page">
        <h2>Security Analysis</h2>
        <p className="subtitle">Loading security scan...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="security-page">
        <h2>Security Analysis</h2>
        <p className="subtitle">
          Unable to load security scan.
        </p>
        <p>{error}</p>
      </div>
    )
  }

  const findings = scan.results || []

  const scannedFiles = scan.paths?.scanned || []

  return (
    <div className="security-page">

      <h2>Security Analysis</h2>

      <p className="subtitle">
        Security scan results for the AUTOFACTORY-2005 legacy code.
      </p>

      <div className="security-summary">

        <div className="security-card">
          <span>Total Findings</span>
          <strong>{findings.length}</strong>
        </div>

        <div className="security-card">
          <span>Files Scanned</span>
          <strong>{scannedFiles.length}</strong>
        </div>

        <div className="security-card">
          <span>Scan Status</span>
          <strong className="success">
            {scan.errors?.length === 0 ? '✓ COMPLETE' : '⚠ ERRORS'}
          </strong>
        </div>

      </div>

      <div className="findings">

        <h3>Security Findings</h3>

        {findings.length === 0 ? (
          <div className="no-findings">
            <strong>✓ No security findings detected</strong>
            <p>
              The current Semgrep scan did not identify any
              matching security issues.
            </p>
          </div>
        ) : (
          findings.map((finding, index) => (
            <div className="finding" key={index}>

              <div className="severity">
                {finding.extra?.severity || 'UNKNOWN'}
              </div>

              <div className="finding-info">
                <strong>
                  {finding.check_id || 'Security Finding'}
                </strong>

                <span>
                  {finding.path}:{finding.start?.line || '—'}
                </span>

                <p>
                  {finding.extra?.message ||
                    'Security issue detected.'}
                </p>
              </div>

            </div>
          ))
        )}

      </div>

    </div>
  )
}

export default SecurityPanel