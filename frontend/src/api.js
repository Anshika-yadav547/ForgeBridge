const API_BASE_URL = 'http://localhost:8000'

export async function askAssistant(question) {
  const response = await fetch(`${API_BASE_URL}/chat`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question: question,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to connect to backend')
  }

  return response.json()
}