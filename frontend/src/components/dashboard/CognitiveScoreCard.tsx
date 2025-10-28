import { Brain } from 'lucide-react'

interface CognitiveScoreCardProps {
  score: number
}

export function CognitiveScoreCard({ score }: CognitiveScoreCardProps) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-500'
    if (score >= 60) return 'text-blue-500'
    if (score >= 40) return 'text-yellow-500'
    return 'text-red-500'
  }

  const getScoreLabel = (score: number) => {
    if (score >= 80) return 'Excellent'
    if (score >= 60) return 'Good'
    if (score >= 40) return 'Fair'
    return 'Needs Attention'
  }

  return (
    <div className="bg-card rounded-lg border border-border p-6">
      <div className="flex items-center gap-2 mb-4">
        <Brain className="h-5 w-5 text-primary" />
        <h3 className="font-semibold">Cognitive Score</h3>
      </div>
      <div className="flex items-end gap-2">
        <span className={`text-5xl font-bold ${getScoreColor(score)}`}>
          {score}
        </span>
        <span className="text-2xl text-muted-foreground mb-1">/100</span>
      </div>
      <p className="text-sm text-muted-foreground mt-2">
        {getScoreLabel(score)}
      </p>
    </div>
  )
}
