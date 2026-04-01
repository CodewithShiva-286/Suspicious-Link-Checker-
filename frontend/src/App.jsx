import { useState } from "react";
import { scanUrl } from "./api";
import LatencyAndHealthBadge from "./components/LatencyAndHealthBadge";
import ReasonPanel from "./components/ReasonPanel";
import ScanProgressTimeline from "./components/ScanProgressTimeline";
import SourceBreakdownGrid from "./components/SourceBreakdownGrid";
import UrlInputForm from "./components/UrlInputForm";
import VerdictCard from "./components/VerdictCard";

export default function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const submitScan = async (url) => {
    setLoading(true);
    setError("");
    try {
      const data = await scanUrl(url);
      setResult(data);
    } catch (err) {
      setError(err.message || "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="app">
      <header>
        <h1>Suspicious Link Checker</h1>
        <p>Service-based URL risk analysis with explainable verdicts.</p>
      </header>

      <UrlInputForm onSubmit={submitScan} loading={loading} />
      {error && <p className="error">{error}</p>}

      {result && (
        <section className="results">
          <div className="results-row results-row--summary">
            <VerdictCard decision={result.decision} />
            <LatencyAndHealthBadge
              durationMs={result.duration_ms}
              providerResults={result.provider_results}
            />
          </div>
          <div className="results-row results-row--timeline">
            <ScanProgressTimeline events={result.timeline_events} />
          </div>
          <div className="results-row results-row--detail">
            <ReasonPanel reasons={result.decision.reasons} />
            <SourceBreakdownGrid providerResults={result.provider_results} />
          </div>
        </section>
      )}
    </main>
  );
}
