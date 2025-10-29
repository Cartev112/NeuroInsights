import { useState, useRef, useEffect, useMemo } from "react"
import {
  Send,
  Loader2,
  Sparkles,
  Brain,
  MessageCircle,
  BarChart3,
  Clock,
} from "lucide-react"
import { chatApi } from "@/services/api"
import type { Message } from "@/types/brain-data"

const SUGGESTIONS = [
  "How did my focus change compared to yesterday?",
  "Summarize my stress patterns over the last week.",
  "When do I enter deep focus most often?",
  "Give me recommendations to improve my creative flow.",
]

const BULLET_PATTERN = /^(-|\*|\u2022)\s*/

const formatLine = (line: string) => line.replace(BULLET_PATTERN, "").trim()

const highlightTokens = (text: string): (string | JSX.Element)[] => {
  if (!text) return [""]
  const regex = /(\d+\.?\d*%|\b\d+\b|deep focus|stress)/gi
  const parts = text.split(regex)
  const matches = text.match(regex)
  const result: (string | JSX.Element)[] = []

  parts.forEach((part, index) => {
    if (part) {
      result.push(part)
    }
    const match = matches?.[index]
    if (match) {
      result.push(
        <span key={`${match}-${index}`} className="font-semibold text-primary">
          {match}
        </span>,
      )
    }
  })

  return result
}

const renderMessageContent = (content: string) => {
  const lines = content.split("\n")
  const blocks: JSX.Element[] = []
  let currentList: string[] = []

  lines.forEach((line, idx) => {
    const trimmed = line.trim()
    const isBullet = BULLET_PATTERN.test(trimmed)

    if (isBullet) {
      currentList.push(formatLine(trimmed))
    } else {
      if (currentList.length > 0) {
        blocks.push(
          <ul key={`list-${idx}`} className="space-y-2">
            {currentList.map((item, itemIdx) => (
              <li key={itemIdx} className="flex items-start gap-2 text-sm text-foreground/90">
                <span className="mt-1 h-2.5 w-2.5 flex-shrink-0 rounded-full bg-primary/70" />
                <span>{highlightTokens(item)}</span>
              </li>
            ))}
          </ul>,
        )
        currentList = []
      }
      if (trimmed.length > 0) {
        blocks.push(
          <p key={`p-${idx}`} className="text-sm leading-relaxed text-foreground/90">
            {highlightTokens(trimmed)}
          </p>,
        )
      }
    }
  })

  if (currentList.length > 0) {
    blocks.push(
      <ul key="list-final" className="space-y-2">
        {currentList.map((item, itemIdx) => (
          <li key={itemIdx} className="flex items-start gap-2 text-sm text-foreground/90">
            <span className="mt-1 h-2.5 w-2.5 flex-shrink-0 rounded-full bg-primary/70" />
            <span>{highlightTokens(item)}</span>
          </li>
        ))}
      </ul>,
    )
  }

  return blocks
}

const MessageBubble = ({ message }: { message: Message }) => {
  const isUser = message.role === "user"

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div className="flex max-w-[75%] items-start gap-3">
        {!isUser && (
          <div className="hidden md:flex h-9 w-9 flex-shrink-0 items-center justify-center rounded-xl bg-primary/25">
            <Brain className="h-5 w-5 text-primary" />
          </div>
        )}
        <div
          className={`group rounded-2xl border px-5 py-4 shadow-lg transition backdrop-blur
            ${
              isUser
                ? "border-white/25 bg-white/15 text-foreground shadow-black/20"
                : "border-primary/40 bg-gradient-to-br from-primary/25 via-primary/15 to-transparent text-foreground shadow-primary/20"
            }
          `}
        >
          <div className="mb-2 flex items-center gap-3">
            <span className="text-xs uppercase tracking-[0.3em] text-primary/80">
              {isUser ? "You" : "NeuroInsights"}
            </span>
            {!isUser && (
              <span className="rounded-full bg-primary/15 px-2 py-0.5 text-[11px] font-medium text-primary">
                Cognitive Coach
              </span>
            )}
          </div>

          <div className="space-y-3 text-foreground/95">{renderMessageContent(message.content)}</div>
        </div>
      </div>
    </div>
  )
}

export function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content:
        "Hi! I'm your NeuroInsights AI assistant. Ask me anything about your brain data. Try questions like:\n\n- \"How was my focus today?\"\n- \"Show me my brain state distribution for the last 7 days\"\n- \"When am I most focused during the day?\"\n- \"Compare my stress levels today vs yesterday\"",
    },
  ])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSend = async () => {
    if (!input.trim() || isLoading) return

    const userMessage: Message = {
      role: "user",
      content: input,
    }

    setMessages((prev) => [...prev, userMessage])
    setInput("")
    setIsLoading(true)

    try {
      const response = await chatApi.sendMessage(userMessage.content)

      const assistantMessage: Message = {
        role: "assistant",
        content: response.response,
      }

      setMessages((prev) => [...prev, assistantMessage])
    } catch (error) {
      console.error("Chat error:", error)
      const errorMessage: Message = {
        role: "assistant",
        content:
          "Sorry, I encountered an error. Please make sure the backend is running and try again.",
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleSuggestionClick = (suggestion: string) => {
    setInput(suggestion)
  }

  const suggestionChips = useMemo(
    () =>
      SUGGESTIONS.map((suggestion) => (
        <button
          key={suggestion}
          onClick={() => handleSuggestionClick(suggestion)}
          className="rounded-full border border-primary/40 bg-primary/15 px-4 py-2 text-sm font-medium text-primary transition hover:border-primary/60 hover:bg-primary/25"
          type="button"
          disabled={isLoading}
        >
          {suggestion}
        </button>
      )),
    [isLoading],
  )

  return (
    <div className="relative flex h-[calc(100vh-12rem)] flex-col overflow-hidden rounded-3xl border border-border/40 bg-card/40 shadow-[0_30px_80px_-40px_rgba(124,58,237,0.45)] backdrop-blur">
      <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(circle_at_20%_20%,rgba(139,92,246,0.15),transparent_45%),radial-gradient(circle_at_80%_30%,rgba(244,114,182,0.12),transparent_45%)]" />

      {/* Header */}
      <div className="relative flex items-center justify-between border-b border-border/40 px-6 py-4">
        <div className="flex items-center gap-4">
          <div className="flex h-12 w-12 items-center justify-center rounded-2xl bg-primary/25 shadow-inner shadow-primary/30">
            <Brain className="h-6 w-6 text-primary" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h3 className="text-xl font-semibold">NeuroInsights Coach</h3>
              <span className="rounded-full bg-primary/20 px-2 py-[2px] text-[11px] font-medium text-primary">
                Live
              </span>
            </div>
            <p className="text-sm text-muted-foreground">
              Ask questions about your cognitive rhythms and get data-backed guidance.
            </p>
          </div>
        </div>
        <div className="hidden lg:flex items-center gap-3 text-xs text-muted-foreground">
          <span className="flex items-center gap-1 rounded-full bg-white/10 px-3 py-1">
            <MessageCircle className="h-3.5 w-3.5 text-primary" />
            Conversational
          </span>
          <span className="flex items-center gap-1 rounded-full bg-white/10 px-3 py-1">
            <BarChart3 className="h-3.5 w-3.5 text-primary" />
            Data aware
          </span>
          <span className="flex items-center gap-1 rounded-full bg-white/10 px-3 py-1">
            <Clock className="h-3.5 w-3.5 text-primary" />
            Real-time
          </span>
        </div>
      </div>

      {/* Suggestions */}
      <div className="relative border-b border-border/30 px-6 py-4">
        <div className="flex flex-wrap gap-3">{suggestionChips}</div>
      </div>

      {/* Messages */}
      <div className="relative flex-1 overflow-y-auto px-6 py-6">
        <div className="flex-1 space-y-5">
          {messages.map((message, index) => (
            <MessageBubble key={index} message={message} />
          ))}
          {isLoading && (
            <div className="flex justify-start">
              <div className="flex items-center gap-3 rounded-2xl border border-primary/40 bg-primary/20 px-5 py-3 text-primary">
                <Loader2 className="h-4 w-4 animate-spin" />
                <span>Analyzing your cognitive signals...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Composer */}
      <div className="relative border-t border-border/40 px-6 py-4">
        <div className="flex items-center gap-3 rounded-full border border-border/40 bg-card/70 px-5 py-3 shadow-lg shadow-primary/10 backdrop-blur">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about your brain data..."
            className="flex-1 bg-transparent text-sm text-foreground placeholder:text-muted-foreground focus:outline-none"
            disabled={isLoading}
          />
          <button
            onClick={handleSend}
            disabled={isLoading || !input.trim()}
            className="flex h-10 w-10 items-center justify-center rounded-full bg-primary text-primary-foreground transition hover:bg-primary/90 disabled:opacity-40"
            type="button"
          >
            <Send className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
