import { ChatInterface } from '@/components/chat/ChatInterface'

export function ChatPage() {
  return (
    <div>
      <div className="mb-6">
        <h2 className="text-3xl font-bold mb-2">Chat with Your Brain Data</h2>
        <p className="text-muted-foreground">
          Ask questions in natural language and get insights about your cognitive patterns.
        </p>
      </div>
      <ChatInterface />
    </div>
  )
}
