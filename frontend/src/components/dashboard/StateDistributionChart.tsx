import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from 'recharts'
import type { StateDistribution } from '@/types/brain-data'

interface StateDistributionChartProps {
  data: StateDistribution | undefined
}

const STATE_COLORS = {
  deep_focus: '#c084fc',
  relaxed: '#93c5fd',
  stressed: '#fb7185',
  creative_flow: '#f9a8d4',
  drowsy: '#fbcfe8',
  distracted: '#a5b4fc',
  neutral: '#ddd6fe',
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
          <Tooltip
            contentStyle={{
              backgroundColor: 'rgba(139, 92, 246, 0.9)',
              border: '1px solid rgba(255, 255, 255, 0.4)',
              borderRadius: '0.5rem',
              color: '#ffffff',
            }}
            formatter={(value: number, name: string) => [
              `${value.toFixed(1)}%`,
              name,
            ]}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
