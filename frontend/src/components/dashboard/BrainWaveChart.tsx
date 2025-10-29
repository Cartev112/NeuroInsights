import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { format, parseISO } from 'date-fns'
import type { BrainDataPoint } from '@/types/brain-data'

interface BrainWaveChartProps {
  data: BrainDataPoint[]
}

const LINE_COLORS = {
  Delta: '#93c5fd',
  Theta: '#a78bfa',
  Alpha: '#f9a8d4',
  Beta: '#c084fc',
  Gamma: '#fda4af',
}

const tooltipStyles = {
  backgroundColor: 'rgba(139, 92, 246, 0.9)',
  border: '1px solid rgba(255, 255, 255, 0.4)',
  borderRadius: '0.75rem',
  color: '#ffffff',
  backdropFilter: 'blur(4px)',
}

export function BrainWaveChart({ data }: BrainWaveChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="bg-card rounded-lg border border-border p-6">
        <h3 className="font-semibold mb-4">Brain Wave Activity</h3>
        <p className="text-muted-foreground">No data available</p>
      </div>
    )
  }

  const chartData = data.map((point) => {
    const timestamp = point.time
    const parsed = typeof timestamp === 'string' ? parseISO(timestamp) : new Date(timestamp)

    return {
      time: format(parsed, 'HH:mm'),
      Delta: point.delta,
      Theta: point.theta,
      Alpha: point.alpha,
      Beta: point.beta,
      Gamma: point.gamma,
    }
  })

  return (
    <div className="bg-card rounded-lg border border-border p-6">
      <h3 className="font-semibold mb-4">Brain Wave Activity</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="4 4" stroke="rgba(255,255,255,0.12)" />
          <XAxis dataKey="time" stroke="rgba(255,255,255,0.6)" />
          <YAxis stroke="rgba(255,255,255,0.6)" />
          <Tooltip
            contentStyle={tooltipStyles}
            labelStyle={{ color: '#fdf4ff', fontWeight: 600 }}
          />
          <Legend
            wrapperStyle={{ color: '#ede9fe' }}
            iconType="circle"
          />
          <Line type="monotone" dataKey="Delta" stroke={LINE_COLORS.Delta} strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Theta" stroke={LINE_COLORS.Theta} strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Alpha" stroke={LINE_COLORS.Alpha} strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Beta" stroke={LINE_COLORS.Beta} strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Gamma" stroke={LINE_COLORS.Gamma} strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
