import { useEffect, useState } from 'react'

function CodebaseMap() {
  const [graph, setGraph] = useState({ nodes: [], edges: [] })
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/architecture')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Failed to load architecture')
        }

        return response.json()
      })
      .then((data) => {
        setGraph(data)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  if (loading) {
    return (
      <div className="codebase-page">
        <h2>Codebase Map</h2>
        <p className="subtitle">Loading architecture...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div className="codebase-page">
        <h2>Codebase Map</h2>
        <p className="subtitle">Unable to load architecture data.</p>
        <p>{error}</p>
      </div>
    )
  }

  const files = graph.nodes.filter(
    (node) =>
      node.type === 'c_file' ||
      node.type === 'cobol_file' ||
      node.type === 'header'
  )

  const functions = graph.nodes.filter(
    (node) =>
      node.type === 'function' ||
      node.type === 'cobol_paragraph'
  )

  const programs = graph.nodes.filter(
    (node) => node.type === 'cobol_program'
  )

  return (
    <div className="codebase-page">
      <h2>Codebase Map</h2>

      <p className="subtitle">
        Explore the structure and dependencies of AUTOFACTORY-2005.
      </p>

      {/* Summary */}
      <div className="architecture-summary">
        <div className="architecture-card">
          <strong>{graph.nodes.length}</strong>
          <span>Total Nodes</span>
        </div>

        <div className="architecture-card">
          <strong>{graph.edges.length}</strong>
          <span>Relationships</span>
        </div>

        <div className="architecture-card">
          <strong>{files.length}</strong>
          <span>Source Files</span>
        </div>
      </div>

      {/* Source files */}
      <section className="architecture-section">
        <h3>Source Files</h3>

        <div className="architecture-grid">
          {files.map((node) => (
            <div className="architecture-node file-node" key={node.id}>
              <div className="node-icon">FILE</div>

              <div>
                <strong>{node.label}</strong>
                <span>{node.type}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Programs */}
      {programs.length > 0 && (
        <section className="architecture-section">
          <h3>Programs</h3>

          <div className="architecture-grid">
            {programs.map((node) => (
              <div className="architecture-node program-node" key={node.id}>
                <div className="node-icon">PROG</div>

                <div>
                  <strong>{node.label}</strong>
                  <span>{node.type}</span>
                </div>
              </div>
            ))}
          </div>
        </section>
      )}

      {/* Functions */}
      <section className="architecture-section">
        <h3>Functions & Paragraphs</h3>

        <div className="architecture-grid">
          {functions.map((node) => (
            <div className="architecture-node function-node" key={node.id}>
              <div className="node-icon">FN</div>

              <div>
                <strong>{node.label}</strong>
                <span>{node.type}</span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Relationships */}
      <section className="architecture-section">
        <h3>Dependencies</h3>

        <div className="dependency-list">
          {graph.edges.map((edge, index) => {
            const source = graph.nodes.find(
              (node) => node.id === edge.source
            )

            const target = graph.nodes.find(
              (node) => node.id === edge.target
            )

            return (
              <div className="dependency" key={index}>
                <strong>{source?.label || edge.source}</strong>

                <span>→</span>

                <strong>{target?.label || edge.target}</strong>

                <small>{edge.kind}</small>
              </div>
            )
          })}
        </div>
      </section>

      <div className="map-legend">
        <strong>Architecture Graph</strong>
        <span>{graph.nodes.length} nodes</span>
        <span>{graph.edges.length} relationships</span>
      </div>
    </div>
  )
}

export default CodebaseMap