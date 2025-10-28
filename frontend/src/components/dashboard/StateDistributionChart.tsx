import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import type { StateDistribution } from '@/types/brain-data'

interface StateDistributionChartProps {
  data: StateDistribution | undefined
}

const STATE_COLORS = {
  deep_focus: '#8b5cf6',
  relaxed: '#3b82f6',
  stressed: '#ef4444',
  creative_flow: '#10b981',
  drowsy: '#f59e0b',
  distracted: '#6b7280',
  neutral: '#9ca3af',
}

const STATE_LABELS = {
  deep_focus: 'Deep Focus',
  relaxed: 'Relaxed',
  stressed: 'Stressed',
  creative_flow: 'Creative Flow',
  drowsy: 'Drowsy',
  distracted: 'Distracted',
  neutral: 'Neutral',
}

export function StateDistributionChart({ data }: StateDistributionChartProps) {
  if (!data) {
    return (
      <div className="bg-card rounded-lg border border-border p-6">
        <h3 className="font-semibold mb-4">State Distribution</h3>
        <p className="text-muted-foreground">No data available</p>
      </div>
    )
  }

  const chartData = Object.entries(data)
    .filter(([_, value]) => value > 0)
    .map(([key, value]) => ({
      name: STATE_LABELS[key as keyof StateDistribution],
      value: value,
      color: STATE_COLORS[key as keyof StateDistribution],
    }))

  return (
    <div className="bg-card rounded-lg border border-border p-6">
      <h3 className="font-semibold mb-4">State Distribution</h3>
      <ResponsiveContainer width="100%" height={250}>
        <PieChart>
          <Pie
            data={chartData}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
            outerRadius={80}
            fill="#8884d8"
            dataKey="value"
          >
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => `${value.toFixed(1)}%`} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
