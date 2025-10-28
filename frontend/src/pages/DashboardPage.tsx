import { useQuery } from '@tanstack/react-query'
import { dataApi } from '@/services/api'
import { StateDistributionChart } from '@/components/dashboard/StateDistributionChart'
import { CognitiveScoreCard } from '@/components/dashboard/CognitiveScoreCard'
import { BrainWaveChart } from '@/components/dashboard/BrainWaveChart'
import { Loader2 } from 'lucide-react'

export function DashboardPage() {
  const now = new Date()
  const startOfDay = new Date(now.getFullYear(), now.getMonth(), now.getDate())
  
  const { data: stateData, isLoading: stateLoading } = useQuery({
    queryKey: ['stateDistribution', 'today'],
    queryFn: () => dataApi.getStateDistribution(
      startOfDay.toISOString(),
      now.toISOString()
    ),
  })

  const { data: scoreData, isLoading: scoreLoading } = useQuery({
    queryKey: ['cognitiveScore', 'today'],
    queryFn: () => dataApi.getCognitiveScore(
      startOfDay.toISOString(),
      now.toISOString()
    ),
  })

  const { data: brainWaveData, isLoading: waveLoading } = useQuery({
    queryKey: ['brainWaves', 'today'],
    queryFn: () => dataApi.getBrainWaves(
      startOfDay.toISOString(),
      now.toISOString(),
      '15min'
    ),
  })

  const isLoading = stateLoading || scoreLoading || waveLoading

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
        <h2 className="text-3xl font-bold mb-2">Dashboard</h2>
        <p className="text-muted-foreground">
          Overview of your cognitive performance today
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {/* Cognitive Score */}
        <CognitiveScoreCard score={scoreData?.cognitive_score || 0} />

        {/* State Distribution */}
        <div className="lg:col-span-2">
          <StateDistributionChart data={stateData} />
        </div>

        {/* Brain Wave Chart */}
        <div className="md:col-span-2 lg:col-span-3">
          <BrainWaveChart data={brainWaveData?.data_points || []} />
        </div>
      </div>
    </div>
  )
}
