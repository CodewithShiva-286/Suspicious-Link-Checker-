const COLORS = {
  safe: "verdict-safe",
  suspicious: "verdict-suspicious",
  malicious: "verdict-malicious",
};

export default function VerdictCard({ decision }) {
  const tone = COLORS[decision?.verdict] || "verdict-default";
  return (
    <section className={`card card--verdict ${tone}`}>
      <h2>Final Verdict</h2>
      <div className="verdict-head">
        <p className="verdict">{decision?.verdict?.toUpperCase() || "N/A"}</p>
        <div className="metric-inline">
          <span className="metric-inline__label">Risk</span>
          <span className="metric-inline__value">
            {decision?.risk_score ?? "-"} / 100
          </span>
          <span className="metric-inline__sep" aria-hidden="true">
            ·
          </span>
          <span className="metric-inline__label">Confidence</span>
          <span className="metric-inline__value">
            {decision?.confidence_score ?? "-"}%
          </span>
        </div>
      </div>
    </section>
  );
}
