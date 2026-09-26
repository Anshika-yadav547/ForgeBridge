import { useState } from 'react'

function Chat() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      text: 'Hello! I can help you understand the AUTOFACTORY-2005 legacy system.'
    }
  ])

  const handleSend = () => {
    if (!question.trim()) return

    setMessages([
      ...messages,
      {
        type: 'user',
        text: question
      }
    ])

    setQuestion('')
  }

  return (
    <div className="chat-page">
      <h2>Legacy System Assistant</h2>

      <p className="subtitle">
        Ask questions about the AUTOFACTORY-2005 legacy system.
      </p>

      <div className="chat-box">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${message.type}`}
          >
            <strong>
              {message.type === 'bot' ? 'ForgeBridge' : 'You'}
            </strong>

            <p>{message.text}</p>
          </div>
        ))}
      </div>

      <div className="chat-input">
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') {
              handleSend()
            }
          }}
          placeholder="Ask about the legacy system..."
        />

        <button onClick={handleSend}>
          Send
        </button>
      </div>
    </div>
  )
}

export default Chat