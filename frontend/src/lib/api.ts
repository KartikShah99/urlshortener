const API = process.env.NEXT_PUBLIC_API_URL || ""

export async function shortenUrl(url: string) {
  const res = await fetch(`${API}/api/shorten`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  })
  if (!res.ok) throw new Error("Failed to shorten")
  return res.json()
}

export async function getStats(shortCode: string) {
  const res = await fetch(`${API}/api/stats/${shortCode}`)
  if (!res.ok) throw new Error("Not found")
  return res.json()
}
