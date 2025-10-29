import { useMemo, useState, useEffect } from "react"
import { useQuery } from "@tanstack/react-query"
import { insightsApi } from "@/services/api"
import {
  Lightbulb,
  TrendingUp,
  Loader2,
  ChevronLeft,
  ChevronRight,
  Sparkles,
} from "lucide-react"

type SectionBlock = {
  title: string
  paragraphs: string[]
  bullets: string[]
}

type Slide = {
  type: "summary" | "metrics" | "tips"
  data?: any
}

const BULLET_REGEX = /^(-|\*|\u2022|\u2013)\s*/

const parseSummarySections = (summary?: string): SectionBlock[] => {
  if (!summary) return []

  const normalized = summary.replace(/\r/g, "")
  const sections = normalized.split(/\n(?=####\s+)/g)

  return sections
    .map((section) => {
      const lines = section.trim().split("\n").filter((line) => line.trim().length > 0)
      const titleLine = lines[0] || ""
      const title = titleLine.replace(/^####\s*/, "").trim()
      const contentLines = lines.slice(1)
      if (!title || contentLines.length === 0) return null

      const paragraphs: string[] = []
      const bullets: string[] = []

      contentLines.forEach((line) => {
        const trimmed = line.trim()
        if (BULLET_REGEX.test(trimmed)) {
          bullets.push(trimmed.replace(BULLET_REGEX, ""))
        } else {
          paragraphs.push(trimmed)
        }
      })

      return { title, paragraphs, bullets }
    })
    .filter((section): section is SectionBlock => section !== null)
}

type SlideContentProps = {
  slide: Slide
  renderSummarySection: (section: SectionBlock) => JSX.Element
  renderMetricsSection: () => JSX.Element | null
  renderTipsSection: () => JSX.Element
}

const SlideContent = ({
  slide,
  renderSummarySection,
  renderMetricsSection,
  renderTipsSection,
}: SlideContentProps) => {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const animation = requestAnimationFrame(() => setVisible(true))
    return () => cancelAnimationFrame(animation)
  }, [])

  return (
    <div
      className={`mx-auto w-full max-w-5xl rounded-3xl border border-border/50 bg-card/70 p-10 shadow-[0_25px_80px_-50px_rgba(124,58,237,0.45)] backdrop-blur transition-all duration-500 ${
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-6"
      }`}
    >
      {slide.type === "summary" && slide.data && renderSummarySection(slide.data)}
      {slide.type === "metrics" && renderMetricsSection()}
      {slide.type === "tips" && (
        <div className="space-y-4">
          <div className="flex items-center gap-3 text-left">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/20">
              <Sparkles className="h-5 w-5 text-primary" />
            </div>
            <h3 className="text-xl font-semibold text-foreground">Quick Tips</h3>
          </div>
          {renderTipsSection()}
        </div>
      )}
    </div>
  )
}

export function InsightsPage() {
  const { data: dailyInsights, isLoading } = useQuery({
    queryKey: ["dailyInsights"],
    queryFn: () => insightsApi.getDailyInsights(),
  })

  const summarySections = useMemo(
    () => parseSummarySections(dailyInsights?.summary),
    [dailyInsights?.summary],
  )

  const slides: Slide[] = useMemo(() => {
    const base: Slide[] = summarySections.map((section) => ({
      type: "summary",
      data: section,
    }))

    if (dailyInsights?.metrics) {
      base.push({ type: "metrics", data: dailyInsights.metrics })
    }

    base.push({ type: "tips" })
    return base
  }, [summarySections, dailyInsights?.metrics])

  const [activeIndex, setActiveIndex] = useState(0)

  const summaryTitle =
    dailyInsights?.summary?.match(/###\s+(.+)/)?.[1] ||
    "Daily Summary of Cognitive Performance"
  const summaryDateLabel = dailyInsights?.date
    ? new Date(dailyInsights.date).toLocaleDateString()
    : undefined

  const renderSummarySection = (section: SectionBlock) => (
    <div className="mx-auto w-full max-w-3xl space-y-5 text-left text-[1.02rem] leading-relaxed text-foreground/95">
      <h4 className="text-lg font-semibold text-primary">{section.title}</h4>
      {section.paragraphs.map((paragraph, index) => (
        <p key={`paragraph-${index}`}>
          {paragraph
            .split(/(\*\*[^*]+\*\*)/)
            .filter(Boolean)
            .map((chunk, i) =>
              chunk.startsWith("**") && chunk.endsWith("**") ? (
                <strong key={`strong-${i}`} className="text-primary">
                  {chunk.slice(2, -2)}
                </strong>
              ) : (
                <span key={`span-${i}`}>{chunk}</span>
              ),
            )}
        </p>
      ))}
      {section.bullets.length > 0 && (
        <ul className="space-y-2">
          {section.bullets.map((bullet, idx) => (
            <li key={`bullet-${idx}`} className="flex items-start gap-3">
              <span className="mt-[6px] h-1.5 w-1.5 flex-shrink-0 rounded-full bg-primary/70" />
              <span>{bullet}</span>
            </li>
          ))}
        </ul>
      )}
    </div>
  )

  const renderMetricsSection = () => {
    const metrics = dailyInsights?.metrics
    if (!metrics) return null

    return (
      <div className="mx-auto grid w-full max-w-4xl gap-6 text-left text-[1.02rem] leading-relaxed text-foreground/95 sm:grid-cols-2">
        <div className="rounded-3xl border border-border/40 bg-secondary/30 p-6 shadow-inner shadow-primary/10">
          <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">Cognitive Score</p>
          <p className="mt-3 text-4xl font-semibold text-primary">{metrics.cognitive_score}</p>
          <p className="mt-3 text-sm text-muted-foreground">
            Composite indicator reflecting focus, stress moderation, and state balance.
          </p>
        </div>
        <div className="rounded-3xl border border-border/40 bg-secondary/30 p-6 shadow-inner shadow-primary/10">
          <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">Focus Time</p>
          <p className="mt-3 text-4xl font-semibold text-primary">
            {metrics.focus_time.toFixed(0)}%
          </p>
          <p className="mt-3 text-sm text-muted-foreground">
            Percentage of the day spent in deep focus and creative flow.
          </p>
        </div>
        <div className="rounded-3xl border border-border/40 bg-secondary/30 p-6 shadow-inner shadow-primary/10">
          <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">Stress Level</p>
          <p className="mt-3 text-4xl font-semibold text-primary">
            {metrics.stress_level.toFixed(0)}%
          </p>
          <p className="mt-3 text-sm text-muted-foreground">
            Lower values indicate calmer transitions between brain states.
          </p>
        </div>
        <div className="rounded-3xl border border-border/40 bg-secondary/30 p-6 shadow-inner shadow-primary/10">
          <p className="text-xs uppercase tracking-[0.3em] text-muted-foreground">Deep Focus</p>
          <p className="mt-3 text-4xl font-semibold text-primary">
            {metrics.state_distribution.deep_focus.toFixed(0)}%
          </p>
          <p className="mt-3 text-sm text-muted-foreground">
            Your strongest contributor to today's productivity.
          </p>
        </div>
      </div>
    )
  }

  const renderTipsSection = () => (
    <div className="mx-auto w-full max-w-3xl space-y-4 text-left text-[1.02rem] leading-relaxed text-foreground/95">
      {[
        "Ask the chat assistant targeted questions to dive deeper into your patterns.",
        "Review your dashboard daily to monitor how focus and stress evolve.",
        "Compare time periods to identify habits that amplify your best cognitive states.",
      ].map((tip, idx) => (
        <div
          key={idx}
          className="flex items-start gap-3 rounded-3xl border border-border/40 bg-secondary/30 p-5 shadow-inner shadow-primary/10"
        >
          <span className="mt-[6px] h-2 w-2 flex-shrink-0 rounded-full bg-primary/70" />
          <p>{tip}</p>
        </div>
      ))}
    </div>
  )

  const currentSlide = slides[activeIndex]

  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <Loader2 className="h-8 w-8 animate-spin text-primary" />
      </div>
    )
  }

  if (!currentSlide) {
    return (
      <div className="flex min-h-[calc(100vh-6rem)] items-center justify-center text-muted-foreground">
        No insights available yet. Start tracking your brain data!
      </div>
    )
  }

  return (
    <div className="flex min-h-[calc(100vh-6rem)] flex-col items-center">
      <div className="w-full max-w-5xl flex-1 px-4">
        <div className="flex flex-col items-center gap-2 py-4 text-center">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-primary/20 shadow-inner shadow-primary/20">
            <Lightbulb className="h-6 w-6 text-primary" />
          </div>
          <div className="space-y-1">
            <p className="text-[11px] uppercase tracking-[0.45em] text-primary/70">
              Daily Summary
            </p>
            <h2 className="text-2xl font-semibold text-foreground">
              {summaryTitle.replace(/^#+\s*/, "")}
            </h2>
            <p className="text-xs text-muted-foreground">
              {summaryDateLabel ? `Generated for ${summaryDateLabel}` : "Latest available insights"}
            </p>
          </div>
        </div>

        <div className="relative">
          <SlideContent
            key={activeIndex}
            slide={currentSlide}
            renderSummarySection={renderSummarySection}
            renderMetricsSection={renderMetricsSection}
            renderTipsSection={renderTipsSection}
          />
        </div>

        <div className="mt-8 flex items-center justify-center gap-6">
          <button
            type="button"
            onClick={() => setActiveIndex((prev) => Math.max(prev - 1, 0))}
            disabled={activeIndex === 0}
            className="flex h-11 w-11 items-center justify-center rounded-full border border-border/50 bg-card/70 text-foreground transition hover:border-primary/50 hover:text-primary disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronLeft className="h-5 w-5" />
          </button>
          <span className="text-sm uppercase tracking-[0.3em] text-muted-foreground">
            {activeIndex + 1} / {slides.length}
          </span>
          <button
            type="button"
            onClick={() => setActiveIndex((prev) => Math.min(prev + 1, slides.length - 1))}
            disabled={activeIndex === slides.length - 1}
            className="flex h-11 w-11 items-center justify-center rounded-full border border-border/50 bg-card/70 text-foreground transition hover:border-primary/50 hover:text-primary disabled:cursor-not-allowed disabled:opacity-40"
          >
            <ChevronRight className="h-5 w-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
