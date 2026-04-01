export default function SourceBreakdownGrid({ providerResults = [] }) {
  return (
    <section className="card">
      <h2>Source Breakdown</h2>
      <div className="source-grid">
        {providerResults.map((source) => (
          <article key={source.source} className={`source ${source.status}`}>
            <header className="source-header">
              <h3>{source.source}</h3>
              <div className="source-metrics">
                <span className="source-pill">{source.status}</span>
                <span>Score {source.score}</span>
                <span>Conf. {source.confidence}%</span>
              </div>
            </header>
            <p className="source-details">{source.details}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
