import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'
import { format, parseISO } from 'date-fns'
import type { BrainDataPoint } from '@/types/brain-data'

interface BrainWaveChartProps {
  data: BrainDataPoint[]
}

export function BrainWaveChart({ data }: BrainWaveChartProps) {
  const parseTimestamp = (value: string) => {
    if (!value) {
      return new Date()
    }

    const normalized = value.endsWith('Z') || value.includes('+') ? value : `${value}Z`
    return parseISO(normalized)
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-card rounded-lg border border-border p-6">
        <h3 className="font-semibold mb-4">Brain Wave Activity</h3>
        <p className="text-muted-foreground">No data available</p>
      </div>
    )
  }

  const chartData = data.map((point) => ({
    time: format(parseTimestamp(point.time), 'HH:mm'),
    Delta: point.delta,
    Theta: point.theta,
    Alpha: point.alpha,
    Beta: point.beta,
    Gamma: point.gamma,
  }))

  return (
    <div className="bg-card rounded-lg border border-border p-6">
      <h3 className="font-semibold mb-4">Brain Wave Activity</h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="Delta" stroke="#6366f1" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Theta" stroke="#8b5cf6" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Alpha" stroke="#3b82f6" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Beta" stroke="#10b981" strokeWidth={2} dot={false} />
          <Line type="monotone" dataKey="Gamma" stroke="#f59e0b" strokeWidth={2} dot={false} />
        </LineChart>
      </ResponsiveContainer>
    </div>
  )
}
