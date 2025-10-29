import { useMemo } from 'react'
import { useQuery } from '@tanstack/react-query'
import { insightsApi } from '@/services/api'
import {
  Lightbulb,
  TrendingUp,
  Loader2,
  Target,
  Sparkles,
  ClipboardCheck,
  Compass,
  Zap,
} from 'lucide-react'

type SectionBlock = {
  title: string
  paragraphs: string[]
  bullets: string[]
}

const iconBySection = (title: string) => {
  const normalized = title.toLowerCase()
  if (normalized.includes('overall')) return <Target className="h-5 w-5 text-primary" />
  if (normalized.includes('highlight')) return <Sparkles className="h-5 w-5 text-primary" />
  if (normalized.includes('improvement')) return <Compass className="h-5 w-5 text-primary" />
  if (normalized.includes('pattern') || normalized.includes('transition'))
    return <Zap className="h-5 w-5 text-primary" />
  if (normalized.includes('recommend')) return <ClipboardCheck className="h-5 w-5 text-primary" />
  return <Lightbulb className="h-5 w-5 text-primary" />
}

const parseSummarySections = (summary?: string): SectionBlock[] => {
  if (!summary) return []

  const normalized = summary.replace(/\r/g, '')
  const sections = normalized.split(/\n(?=####\s+)/g)

  return sections
    .map((section) => {
      const lines = section.trim().split('\n').filter((line) => line.trim().length > 0)
      const titleLine = lines[0] || ''
      const title = titleLine.replace(/^####\s*/, '').trim()
      const contentLines = lines.slice(1)
      if (!title || contentLines.length === 0) return null

      const paragraphs: string[] = []
      const bullets: string[] = []

      contentLines.forEach((line) => {
        const trimmed = line.trim()
        if (/^[-–•]/.test(trimmed)) {
          bullets.push(trimmed.replace(/^[-–•]\s*/, ''))
        } else {
          paragraphs.push(trimmed)
        }
      })

      return { title, paragraphs, bullets }
    })
    .filter((section): section is SectionBlock => section !== null)
}

const DailySectionCard = ({ section }: { section: SectionBlock }) => (
  <div className="rounded-2xl border border-border/50 bg-card/70 p-6 shadow-lg shadow-primary/10 backdrop-blur transition hover:border-primary/60 hover:shadow-primary/20">
    <div className="flex items-center gap-3 mb-4">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/15">
        {iconBySection(section.title)}
      </div>
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-primary/70">Insight</p>
        <h4 className="text-lg font-semibold text-foreground">{section.title}</h4>
      </div>
    </div>

    <div className="space-y-3 text-sm leading-relaxed text-foreground/95">
      {section.paragraphs.map((paragraph, index) => (
        <p key={`p-${index}`} className="text-foreground/90">
          {paragraph}
        </p>
      ))}

      {section.bullets.length > 0 && (
        <ul className="space-y-2">
          {section.bullets.map((bullet, idx) => (
            <li key={`b-${idx}`} className="flex items-start gap-3 text-foreground/90">
              <span className="mt-1 h-2.5 w-2.5 flex-shrink-0 rounded-full bg-primary/70" />
              <span>{bullet}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  </div>
)

export function InsightsPage() {
  const { data: dailyInsights, isLoading } = useQuery({
    queryKey: ['dailyInsights'],
    queryFn: () => insightsApi.getDailyInsights(),
  })

  const sections = useMemo(
    () => parseSummarySections(dailyInsights?.summary),
    [dailyInsights?.summary],
  )
  const headline = dailyInsights?.summary?.match(/###\s+(.+)/)?.[1]

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  return (
    <div>
      <div className="mb-8">
        <h2 className="text-3xl font-bold mb-2">Insights</h2>
        <p className="text-muted-foreground">
          AI-generated insights about your cognitive patterns
        </p>
      </div>

      <div className="space-y-8">
        {/* Daily Summary */}
        <div className="rounded-3xl border border-border/40 bg-card/60 p-6 shadow-xl shadow-primary/15 backdrop-blur">
          <div className="flex items-start justify-between gap-4">
            <div className="flex items-center gap-3">
              <div className="flex h-11 w-11 items-center justify-center rounded-2xl bg-primary/20">
                <Lightbulb className="h-6 w-6 text-primary" />
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-primary/70">Daily Summary</p>
                <h3 className="text-2xl font-semibold text-foreground">
                  {headline ?? 'Insightful Moments'}
                </h3>
                <p className="mt-1 text-sm text-muted-foreground">
                  {dailyInsights?.date
                    ? `Generated for ${new Date(dailyInsights.date).toLocaleDateString()}`
                    : 'Up-to-the-minute reflections on your cognitive patterns.'}
                </p>
              </div>
            </div>
          </div>

          <div className="mt-6 grid gap-5 lg:grid-cols-2">
            {sections.length > 0 ? (
              sections.map((section) => (
                <DailySectionCard key={section.title} section={section} />
              ))
            ) : (
              <div className="rounded-2xl border border-dashed border-border/40 p-6 text-sm text-muted-foreground">
                No insights available yet. Start tracking your brain data!
              </div>
            )}
          </div>
        </div>

        {/* Metrics */}
        {dailyInsights?.metrics && (
          <div className="rounded-3xl border border-border/40 bg-card/60 p-6 shadow-lg shadow-primary/15 backdrop-blur">
            <div className="flex items-center gap-3 mb-6">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/20">
                <TrendingUp className="h-5 w-5 text-primary" />
              </div>
              <div>
                <p className="text-xs uppercase tracking-[0.3em] text-primary/70">Momentum</p>
                <h3 className="text-xl font-semibold">Today's Metrics</h3>
              </div>
            </div>

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-4">
              <div className="rounded-2xl border border-border/50 bg-secondary/40 p-5 text-foreground">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                  Cognitive Score
                </p>
                <p className="mt-2 text-3xl font-semibold text-primary">
                  {dailyInsights.metrics.cognitive_score}
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Composite score of focus, balance, and stress moderation.
                </p>
              </div>

              <div className="rounded-2xl border border-border/50 bg-secondary/40 p-5 text-foreground">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                  Focus Time
                </p>
                <p className="mt-2 text-3xl font-semibold text-primary">
                  {dailyInsights.metrics.focus_time.toFixed(0)}%
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Time spent in deep focus and creative flow states.
                </p>
              </div>

              <div className="rounded-2xl border border-border/50 bg-secondary/40 p-5 text-foreground">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                  Stress Level
                </p>
                <p className="mt-2 text-3xl font-semibold text-primary">
                  {dailyInsights.metrics.stress_level.toFixed(0)}%
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Staying low here means smoother cognitive transitions.
                </p>
              </div>

              <div className="rounded-2xl border border-border/50 bg-secondary/40 p-5 text-foreground">
                <p className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
                  Deep Focus
                </p>
                <p className="mt-2 text-3xl font-semibold text-primary">
                  {dailyInsights.metrics.state_distribution.deep_focus.toFixed(0)}%
                </p>
                <p className="mt-2 text-xs text-muted-foreground">
                  Anchor state powering your peak productivity.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Tips */}
        <div className="rounded-3xl border border-border/40 bg-card/60 p-6 shadow-lg shadow-primary/15 backdrop-blur">
          <div className="mb-4 flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/20">
              <Sparkles className="h-5 w-5 text-primary" />
            </div>
            <div>
              <p className="text-xs uppercase tracking-[0.3em] text-primary/70">Keep Momentum</p>
              <h3 className="text-xl font-semibold">Quick Tips</h3>
            </div>
          </div>
          <ul className="grid gap-3 md:grid-cols-3">
            {[
              'Ask the chat assistant targeted questions to dive deeper into your patterns.',
              'Review your dashboard daily to monitor how focus and stress evolve.',
              'Compare time periods to identify habits that amplify your best cognitive states.',
            ].map((tip, idx) => (
              <li
                key={idx}
                className="group rounded-2xl border border-border/30 bg-secondary/30 p-4 transition hover:border-primary/50 hover:bg-secondary/60"
              >
                <div className="flex items-start gap-3">
                  <span className="mt-1 h-2.5 w-2.5 flex-shrink-0 rounded-full bg-primary/70 transition group-hover:bg-primary" />
                  <p className="text-sm text-foreground/90">{tip}</p>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  )
}
