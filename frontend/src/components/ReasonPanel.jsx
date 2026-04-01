export default function ReasonPanel({ reasons = [] }) {
  return (
    <section className="card card--reasons">
      <h2>Detailed Reasoning</h2>
      <ul className="reason-list">
        {reasons.map((reason, idx) => (
          <li key={`${reason}-${idx}`}>{reason}</li>
        ))}
      </ul>
    </section>
  );
}
