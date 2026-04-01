export default function LatencyAndHealthBadge({ durationMs, providerResults = [] }) {
  const degraded = providerResults.some((item) => item.status === "unknown");
  return (
    <section className="card card--health">
      <h2>Scan Health</h2>
      <div className="metric-inline metric-inline--stack">
        <span className="metric-inline__label">Duration</span>
        <span className="metric-inline__value">{durationMs ?? "-"} ms</span>
        <span className="metric-inline__sep" aria-hidden="true">
          ·
        </span>
        <span className="metric-inline__label">Mode</span>
        <span className="metric-inline__value metric-inline__value--wrap">
          {degraded ? "Degraded (partial provider coverage)" : "Full coverage"}
        </span>
      </div>
    </section>
  );
}
