const API_BASE_URL = 'http://127.0.0.1:8000'

export async function getMachineStatus(machineId = 7) {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/machines/${machineId}/status`
  )

  if (!response.ok) {
    throw new Error('Failed to fetch machine status')
  }

  return response.json()
}

export async function askAssistant(question) {
  const response = await fetch(`${API_BASE_URL}/api/analyze`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      question,
    }),
  })

  if (!response.ok) {
    throw new Error('Failed to analyze question')
  }

  return response.json()
}