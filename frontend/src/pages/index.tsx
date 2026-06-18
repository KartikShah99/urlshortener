import { useState } from "react"
import { shortenUrl, getStats } from "../lib/api"

export default function Home() {
  const [url, setUrl] = useState("")
  const [result, setResult] = useState<{ short_url: string; short_code: string } | null>(null)
  const [stats, setStats] = useState<{ clicks: number } | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [copied, setCopied] = useState(false)

  const handleShorten = async () => {
    if (!url) return
    setLoading(true)
    setError(null)
    setResult(null)
    setStats(null)
    try {
      const data = await shortenUrl(url)
      setResult(data)
    } catch {
      setError("Failed to shorten URL. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleCopy = () => {
    if (!result) return
    const el = document.createElement("textarea")
    el.value = result.short_url
    document.body.appendChild(el)
    el.select()
    document.execCommand("copy")
    document.body.removeChild(el)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const handleStats = async () => {
    if (!result) return
    try {
      const data = await getStats(result.short_code)
      setStats(data)
    } catch {
      setError("Could not fetch stats.")
    }
  }

  return (
    <main style={{ maxWidth: 620, margin: "80px auto", padding: 24, fontFamily: "system-ui, sans-serif" }}>
      <h1 style={{ fontSize: 28, marginBottom: 8 }}>🔗 URL Shortener</h1>
      <p style={{ color: "#666", marginBottom: 24 }}>Paste a long URL and get a short one instantly.</p>

      <div style={{ display: "flex", gap: 8, marginBottom: 16 }}>
        <input
          value={url}
          onChange={e => setUrl(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleShorten()}
          placeholder="https://your-very-long-url.com/..."
          style={{
            flex: 1, padding: "12px 14px", fontSize: 15,
            border: "1px solid #ddd", borderRadius: 8, outline: "none"
          }}
        />
        <button
          onClick={handleShorten}
          disabled={loading}
          style={{
            padding: "12px 20px", background: "#5c6ef8", color: "#fff",
            border: "none", borderRadius: 8, cursor: "pointer", fontSize: 15,
            opacity: loading ? 0.7 : 1
          }}
        >
          {loading ? "..." : "Shorten"}
        </button>
      </div>

      {error && (
        <div style={{ padding: 12, background: "#fff0f0", borderRadius: 8, color: "#c00", marginBottom: 16 }}>
          {error}
        </div>
      )}

      {result && (
        <div style={{ padding: 20, background: "#f0f4ff", borderRadius: 10, marginBottom: 16 }}>
          <p style={{ margin: "0 0 8px", fontSize: 13, color: "#555" }}>Your short URL:</p>
          
            <a href={result.short_url}
            target="_blank"
            rel="noreferrer"
            style={{ fontSize: 20, fontWeight: 600, color: "#5c6ef8", wordBreak: "break-all" }}
          >
            {result.short_url}
          </a>
          <div style={{ marginTop: 16, display: "flex", gap: 8, alignItems: "center" }}>
            <button
              onClick={handleCopy}
              style={{
                padding: "8px 14px",
                background: copied ? "#4caf50" : "#fff",
                color: copied ? "#fff" : "#333",
                border: "1px solid #ddd", borderRadius: 6, cursor: "pointer"
              }}
            >
              {copied ? "Copied!" : "Copy"}
            </button>
            <button
              onClick={handleStats}
              style={{ padding: "8px 14px", background: "#fff", border: "1px solid #ddd", borderRadius: 6, cursor: "pointer" }}
            >
              View Stats
            </button>
          </div>
          {stats && (
            <p style={{ marginTop: 12, fontSize: 14, color: "#444" }}>
              Total clicks: <strong>{stats.clicks}</strong>
            </p>
          )}
        </div>
      )}
    </main>
  )
}
