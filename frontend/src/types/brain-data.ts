export interface BrainWaveData {
  delta: number
  theta: number
  alpha: number
  beta: number
  gamma: number
}

export interface BrainDataPoint extends BrainWaveData {
  time: string
  state?: string
  confidence?: number
}

export interface StateDistribution {
  deep_focus: number
  relaxed: number
  stressed: number
  creative_flow: number
  drowsy: number
  distracted: number
  neutral: number
}

export interface CognitiveScore {
  cognitive_score: number
  start_time: string
  end_time: string
}

export interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export interface ChatResponse {
  response: string
  metadata?: {
    tool_calls_made?: number
  }
}

export interface DailyInsight {
  date: string
  summary: string
  metrics: {
    cognitive_score: number
    state_distribution: StateDistribution
    focus_time: number
    stress_level: number
  }
}
