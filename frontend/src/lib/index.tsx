import { useState } from "react"
import { shortenUrl } from "../lib/api"

export default function Home() {
  const [url, setUrl] = useState("")
  const [result, setResult] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)

  const handleSubmit = async () => {
    setLoading(true)
    try {
      const data = await shortenUrl(url)
      setResult(data.short_url)
    } finally {
      setLoading(false)
    }
  }

  return (
    <main style={{ maxWidth: 600, margin: "80px auto", padding: 24 }}>
      <h1>URL Shortener</h1>
      <input
        value={url}
        onChange={e => setUrl(e.target.value)}
        placeholder="https://your-long-url.com/..."
        style={{ width: "100%", padding: 12, fontSize: 16, marginBottom: 12 }}
      />
      <button onClick={handleSubmit} disabled={loading}>
        {loading ? "Shortening..." : "Shorten"}
      </button>
      {result && (
        <div style={{ marginTop: 24 }}>
          <p>Your short URL:</p>
          <a href={result} target="_blank">{result}</a>
        </div>
      )}
    </main>
  )
}
