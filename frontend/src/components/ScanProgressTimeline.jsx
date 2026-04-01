export default function ScanProgressTimeline({ events = [] }) {
  return (
    <section className="card timeline">
      <h2>Scan Timeline</h2>
      <ul>
        {events.map((event, idx) => (
          <li key={`${event.event}-${idx}`}>
            <span className="dot" />
            <div>
              <strong>{event.event}</strong>
              <p>
                {event.source}: {event.message}
              </p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
