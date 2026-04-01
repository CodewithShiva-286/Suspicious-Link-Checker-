import { useState } from "react";

export default function UrlInputForm({ onSubmit, loading }) {
  const [url, setUrl] = useState("");

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit(url);
  };

  return (
    <form className="url-form" onSubmit={handleSubmit}>
      <input
        type="url"
        value={url}
        onChange={(event) => setUrl(event.target.value)}
        placeholder="https://example.com"
        required
      />
      <button type="submit" disabled={loading}>
        {loading ? "Scanning..." : "Scan URL"}
      </button>
    </form>
  );
}
