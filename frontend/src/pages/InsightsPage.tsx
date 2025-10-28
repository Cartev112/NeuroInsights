import { useQuery } from '@tanstack/react-query'
import { insightsApi } from '@/services/api'
import { Lightbulb, TrendingUp, Loader2 } from 'lucide-react'

export function InsightsPage() {
  const { data: dailyInsights, isLoading } = useQuery({
    queryKey: ['dailyInsights'],
    queryFn: () => insightsApi.getDailyInsights(),
  })

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  return (
    <div>
      <div className="mb-6">
        <h2 className="text-3xl font-bold mb-2">Insights</h2>
        <p className="text-muted-foreground">
          AI-generated insights about your cognitive patterns
        </p>
      </div>

      <div className="space-y-6">
        {/* Daily Summary */}
        <div className="bg-card rounded-lg border border-border p-6">
          <div className="flex items-center gap-2 mb-4">
            <Lightbulb className="h-6 w-6 text-primary" />
            <h3 className="text-xl font-semibold">Daily Summary</h3>
          </div>
          <div className="prose prose-sm max-w-none">
            <p className="whitespace-pre-wrap text-foreground">
              {dailyInsights?.summary || 'No insights available yet. Start tracking your brain data!'}
            </p>
          </div>
        </div>

        {/* Metrics */}
        {dailyInsights?.metrics && (
          <div className="bg-card rounded-lg border border-border p-6">
            <div className="flex items-center gap-2 mb-4">
              <TrendingUp className="h-6 w-6 text-primary" />
              <h3 className="text-xl font-semibold">Today's Metrics</h3>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-muted rounded-lg p-4">
                <p className="text-sm text-muted-foreground mb-1">Cognitive Score</p>
                <p className="text-3xl font-bold text-primary">
                  {dailyInsights.metrics.cognitive_score}
                </p>
              </div>
              <div className="bg-muted rounded-lg p-4">
                <p className="text-sm text-muted-foreground mb-1">Focus Time</p>
                <p className="text-3xl font-bold text-primary">
                  {dailyInsights.metrics.focus_time.toFixed(0)}%
                </p>
              </div>
              <div className="bg-muted rounded-lg p-4">
                <p className="text-sm text-muted-foreground mb-1">Stress Level</p>
                <p className="text-3xl font-bold text-primary">
                  {dailyInsights.metrics.stress_level.toFixed(0)}%
                </p>
              </div>
              <div className="bg-muted rounded-lg p-4">
                <p className="text-sm text-muted-foreground mb-1">Deep Focus</p>
                <p className="text-3xl font-bold text-primary">
                  {dailyInsights.metrics.state_distribution.deep_focus.toFixed(0)}%
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Tips */}
        <div className="bg-card rounded-lg border border-border p-6">
          <h3 className="text-xl font-semibold mb-4">Quick Tips</h3>
          <ul className="space-y-2">
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Ask the chat assistant specific questions about your patterns</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Check your dashboard regularly to track cognitive trends</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="text-primary">•</span>
              <span>Compare different time periods to identify what works best for you</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  )
}
