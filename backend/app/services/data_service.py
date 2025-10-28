"""Service for brain data operations"""

from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import UUID
import json

from app.core.mock_data.generators import mock_data_provider
from app.models.schemas import BrainDataPointResponse, StateDistribution


class DataService:
    """Service for retrieving and processing brain data"""
    
    def __init__(self):
        self.mock_provider = mock_data_provider
    
    async def get_brain_data(
        self,
        user_id: UUID,
        start_time: datetime,
        end_time: datetime,
        granularity: str = "minute"
    ) -> List[Dict[str, Any]]:
        """
        Get brain data for a time range
        """
        
        # For now, generate mock data on the fly
        generator = self.mock_provider.get_generator(user_id)
        
        duration_minutes = int((end_time - start_time).total_seconds() / 60)
        
        # Generate session
        session = generator.generate_custom_session(
            duration_minutes=duration_minutes,
            primary_state='deep_focus',
            start_time=start_time,
            include_transitions=True
        )
        
        # Apply granularity
        if granularity != "minute":
            session['data_points'] = self._aggregate_data(
                session['data_points'],
                granularity
            )
        
        return session['data_points']
    
    async def get_state_distribution(
        self,
        user_id: UUID,
        start_time: datetime,
        end_time: datetime
    ) -> StateDistribution:
        """
        Get distribution of cognitive states over a time period
        """
        
        data_points = await self.get_brain_data(user_id, start_time, end_time)
        
        # Count states
        state_counts = {
            'deep_focus': 0,
            'relaxed': 0,
            'stressed': 0,
            'creative_flow': 0,
            'drowsy': 0,
            'distracted': 0,
            'neutral': 0
        }
        
        for point in data_points:
            state = point.get('state', 'neutral')
            if state in state_counts:
                state_counts[state] += 1
        
        # Convert to percentages
        total = len(data_points)
        if total > 0:
            distribution = {
                state: round(count / total * 100, 1)
                for state, count in state_counts.items()
            }
        else:
            distribution = state_counts
        
        return StateDistribution(**distribution)
    
    async def get_cognitive_score(
        self,
        user_id: UUID,
        start_time: datetime,
        end_time: datetime
    ) -> int:
        """
        Calculate cognitive fitness score (0-100)
        """
        
        data_points = await self.get_brain_data(user_id, start_time, end_time)
        distribution = await self.get_state_distribution(user_id, start_time, end_time)
        
        # Calculate score based on:
        # - Focus time (deep_focus + creative_flow)
        # - Low stress
        # - State balance (not too much drowsy or distracted)
        
        focus_score = (distribution.deep_focus + distribution.creative_flow) * 0.5
        stress_penalty = distribution.stressed * 0.8
        drowsy_penalty = distribution.drowsy * 0.6
        distracted_penalty = distribution.distracted * 0.4
        
        score = 50 + focus_score - stress_penalty - drowsy_penalty - distracted_penalty
        score = max(0, min(100, int(score)))
        
        return score
    
    async def compare_time_periods(
        self,
        user_id: UUID,
        period1_start: datetime,
        period1_end: datetime,
        period2_start: datetime,
        period2_end: datetime,
        metric: str = "all"
    ) -> Dict[str, Any]:
        """
        Compare brain patterns between two time periods
        """
        
        # Get data for both periods
        dist1 = await self.get_state_distribution(user_id, period1_start, period1_end)
        dist2 = await self.get_state_distribution(user_id, period2_start, period2_end)
        
        score1 = await self.get_cognitive_score(user_id, period1_start, period1_end)
        score2 = await self.get_cognitive_score(user_id, period2_start, period2_end)
        
        comparison = {
            "period1": {
                "start": period1_start.isoformat(),
                "end": period1_end.isoformat(),
                "cognitive_score": score1,
                "state_distribution": dist1.model_dump()
            },
            "period2": {
                "start": period2_start.isoformat(),
                "end": period2_end.isoformat(),
                "cognitive_score": score2,
                "state_distribution": dist2.model_dump()
            },
            "changes": {
                "cognitive_score_change": score1 - score2,
                "focus_change": dist1.deep_focus - dist2.deep_focus,
                "stress_change": dist1.stressed - dist2.stressed
            }
        }
        
        return comparison
    
    async def find_patterns(
        self,
        user_id: UUID,
        pattern_type: str,
        start_time: datetime,
        end_time: datetime,
        activity: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Find patterns in brain data
        """
        
        if pattern_type == "time_of_day":
            return await self._find_time_of_day_patterns(user_id, start_time, end_time)
        elif pattern_type == "focus_windows":
            return await self._find_focus_windows(user_id, start_time, end_time)
        else:
            return {"pattern_type": pattern_type, "message": "Pattern analysis coming soon"}
    
    async def _find_time_of_day_patterns(
        self,
        user_id: UUID,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """
        Find patterns by time of day
        """
        
        # Analyze by hour of day
        hourly_scores = {}
        
        current = start_time
        while current < end_time:
            hour = current.hour
            hour_end = current + timedelta(hours=1)
            
            score = await self.get_cognitive_score(user_id, current, hour_end)
            
            if hour not in hourly_scores:
                hourly_scores[hour] = []
            hourly_scores[hour].append(score)
            
            current = hour_end
        
        # Average by hour
        avg_by_hour = {
            hour: sum(scores) / len(scores)
            for hour, scores in hourly_scores.items()
        }
        
        # Find best hours
        best_hours = sorted(avg_by_hour.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "pattern_type": "time_of_day",
            "hourly_scores": avg_by_hour,
            "best_hours": [
                {"hour": hour, "score": score}
                for hour, score in best_hours
            ]
        }
    
    async def _find_focus_windows(
        self,
        user_id: UUID,
        start_time: datetime,
        end_time: datetime
    ) -> Dict[str, Any]:
        """
        Find windows of sustained focus
        """
        
        data_points = await self.get_brain_data(user_id, start_time, end_time)
        
        # Find consecutive focus periods
        focus_windows = []
        current_window = None
        
        for point in data_points:
            if point.get('state') in ['deep_focus', 'creative_flow']:
                if current_window is None:
                    current_window = {
                        'start': point['time'],
                        'end': point['time'],
                        'duration': 1
                    }
                else:
                    current_window['end'] = point['time']
                    current_window['duration'] += 1
            else:
                if current_window and current_window['duration'] >= 15:  # At least 15 minutes
                    focus_windows.append(current_window)
                current_window = None
        
        # Add last window if exists
        if current_window and current_window['duration'] >= 15:
            focus_windows.append(current_window)
        
        return {
            "pattern_type": "focus_windows",
            "windows": focus_windows,
            "total_focus_time": sum(w['duration'] for w in focus_windows),
            "avg_window_duration": sum(w['duration'] for w in focus_windows) / len(focus_windows) if focus_windows else 0
        }
    
    def _aggregate_data(
        self,
        data_points: List[Dict[str, Any]],
        granularity: str
    ) -> List[Dict[str, Any]]:
        """
        Aggregate data points by granularity
        """
        
        if granularity == "minute":
            return data_points
        
        # Determine window size
        window_minutes = {
            "5min": 5,
            "15min": 15,
            "hour": 60
        }.get(granularity, 5)
        
        aggregated = []
        i = 0
        
        while i < len(data_points):
            window = data_points[i:i + window_minutes]
            if not window:
                break
            
            # Average the values
            avg_point = {
                'time': window[0]['time'],
                'delta': sum(p['delta'] for p in window) / len(window),
                'theta': sum(p['theta'] for p in window) / len(window),
                'alpha': sum(p['alpha'] for p in window) / len(window),
                'beta': sum(p['beta'] for p in window) / len(window),
                'gamma': sum(p['gamma'] for p in window) / len(window),
                'state': window[len(window) // 2].get('state'),  # Middle state
            }
            
            aggregated.append(avg_point)
            i += window_minutes
        
        return aggregated


# Singleton instance
_data_service: Optional[DataService] = None


def get_data_service() -> DataService:
    """Get or create data service instance"""
    global _data_service
    if _data_service is None:
        _data_service = DataService()
    return _data_service
