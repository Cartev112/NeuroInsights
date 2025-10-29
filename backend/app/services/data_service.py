"""Service for brain data operations"""

from collections import defaultdict
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from uuid import UUID
import json
import random
import logging

from app.core.mock_data.generators import mock_data_provider
from app.models.schemas import BrainDataPointResponse, StateDistribution

logger = logging.getLogger(__name__)


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
        
        logger.debug(
            "get_brain_data called",
            extra={
                "user_id": str(user_id),
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "granularity": granularity,
            },
        )

        # Calculate duration
        duration_minutes = int((end_time - start_time).total_seconds() / 60)
        logger.debug("Initial duration_minutes=%s", duration_minutes)
        
        # Ensure minimum duration
        if duration_minutes < 1:
            duration_minutes = 1
            logger.debug("Duration adjusted to minimum minute: %s", duration_minutes)
        
        # Get generator
        generator = self.mock_provider.get_generator(user_id)
        
        # For today's data, use a realistic scenario
        # Check if this is "today" based on the start_time
        is_today = start_time.date() == datetime.now().date()
        
        if is_today and duration_minutes > 60:
            # Use a pre-built scenario for a more realistic day
            scenarios = ['typical_workday', 'productive_morning', 'creative_work']
            scenario_name = random.choice(scenarios)
            logger.debug("Using scenario %s for today's data", scenario_name)
            
            # Generate from scenario but adjust to requested time range
            from app.core.mock_data.patterns import SCENARIOS
            scenario = SCENARIOS.get(scenario_name, SCENARIOS['typical_workday'])
            
            # If requested duration is less than scenario, truncate
            if duration_minutes < scenario['duration']:
                session = generator.generate_session_from_scenario(
                    scenario_name,
                    start_time
                )
                # Truncate data points to requested duration
                session['data_points'] = [
                    p for p in session['data_points']
                    if p['time'] < end_time
                ]
                logger.debug(
                    "Truncated scenario points",
                    extra={
                        "requested_duration": duration_minutes,
                        "scenario_duration": scenario['duration'],
                        "points_after": len(session['data_points']),
                    },
                )
            else:
                session = generator.generate_session_from_scenario(
                    scenario_name,
                    start_time
                )
        else:
            # Generate custom session with varied states
            primary_states = ['deep_focus', 'relaxed', 'creative_flow', 'neutral']
            primary_state = random.choice(primary_states)
            logger.debug("Using custom session with primary_state=%s", primary_state)
            
            session = generator.generate_custom_session(
                duration_minutes=duration_minutes,
                primary_state=primary_state,
                start_time=start_time,
                include_transitions=True
            )
        
        # Apply granularity
        if granularity != "minute":
            session['data_points'] = self._aggregate_data(
                session['data_points'],
                granularity
            )
            logger.debug(
                "Aggregated data points",
                extra={
                    "granularity": granularity,
                    "points": len(session['data_points']),
                },
            )
        else:
            logger.debug("Generated raw data points: %s", len(session['data_points']))
        
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
        logger.debug("Calculating state distribution for %s points", len(data_points))
        
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
            # Return default distribution if no data
            distribution = {
                'deep_focus': 25.0,
                'relaxed': 20.0,
                'stressed': 10.0,
                'creative_flow': 15.0,
                'drowsy': 10.0,
                'distracted': 10.0,
                'neutral': 10.0
            }
        
        result = StateDistribution(**distribution)
        logger.debug("State distribution result: %s", result.model_dump())
        return result
    
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
        logger.debug("Calculating cognitive score with %s data points", len(data_points))
        
        if not data_points:
            logger.debug("No data points found; returning default cognitive score")
            return 70  # Default score
        
        distribution = await self.get_state_distribution(user_id, start_time, end_time)
        logger.debug("Distribution for score calc: %s", distribution.model_dump())
        
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
        logger.debug("Computed cognitive score: %s", score)
        
        return score

    async def get_activities(
        self,
        user_id: UUID,
        start_time: datetime,
        end_time: datetime,
        min_duration_minutes: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Build activity timeline within a window.
        Groups consecutive minutes that share the same activity label (or inferred label).
        """

        data_points = await self.get_brain_data(
            user_id,
            start_time,
            end_time,
            granularity="minute"
        )

        if not data_points:
            logger.debug("No data points available for activity timeline.")
            return []

        normalized_points = []
        for point in data_points:
            point_time = point.get("time")
            if isinstance(point_time, str):
                try:
                    point_time = datetime.fromisoformat(point_time)
                except ValueError:
                    logger.debug("Failed ISO parse for point time %s; skipping point.", point.get("time"))
                    continue
            if not isinstance(point_time, datetime):
                continue

            normalized_point = dict(point)
            normalized_point["time"] = point_time
            normalized_point["activity"] = normalized_point.get("activity")
            normalized_point["state"] = normalized_point.get("state") or "unknown"
            if not normalized_point["activity"]:
                normalized_point["activity"] = self._infer_activity_from_state(normalized_point["state"])
                normalized_point["_activity_source"] = "inferred"
            else:
                normalized_point["_activity_source"] = "scenario"
            normalized_point["confidence"] = normalized_point.get("confidence", 0.7)

            normalized_points.append(normalized_point)

        if not normalized_points:
            return []

        normalized_points.sort(key=lambda p: p["time"])

        activities: List[Dict[str, Any]] = []
        current_segment: Optional[Dict[str, Any]] = None

        def finalize_segment(segment: Optional[Dict[str, Any]]):
            if not segment:
                return

            duration_minutes = max(
                1,
                round(
                    (segment["end_time"] - segment["start_time"]).total_seconds() / 60
                ),
            )

            if duration_minutes < max(1, min_duration_minutes):
                logger.debug(
                    "Discarding short activity segment %s lasting %s minutes",
                    segment["activity"],
                    duration_minutes,
                )
                return

            total_state_counts = sum(segment["state_counts"].values())
            if total_state_counts == 0:
                total_state_counts = 1  # avoid division by zero

            state_distribution = {
                state: round(count / total_state_counts * 100, 1)
                for state, count in segment["state_counts"].items()
            }

            dominant_state = max(
                segment["state_counts"],
                key=lambda state: segment["state_counts"][state],
                default="unknown",
            )

            focus_minutes = (
                segment["state_counts"].get("deep_focus", 0)
                + segment["state_counts"].get("creative_flow", 0)
            )
            focus_percentage = round(focus_minutes / total_state_counts * 100, 1)

            avg_confidence = round(
                segment["confidence_total"] / max(1, segment["points_count"]), 2
            )

            activities.append(
                {
                    "activity": segment["activity"],
                    "start_time": segment["start_time"].isoformat(),
                    "end_time": segment["end_time"].isoformat(),
                    "duration_minutes": duration_minutes,
                    "state_distribution": state_distribution,
                    "dominant_state": dominant_state,
                    "focus_percentage": focus_percentage,
                    "average_confidence": avg_confidence,
                    "source": segment["activity_source"],
                }
            )

        for point in normalized_points:
            activity_name = point["activity"]
            state = point["state"]
            timestamp = point["time"]
            minute_end = min(timestamp + timedelta(minutes=1), end_time)

            if current_segment and activity_name == current_segment["activity"]:
                current_segment["end_time"] = minute_end
                current_segment["state_counts"][state] += 1
                current_segment["confidence_total"] += point["confidence"]
                current_segment["points_count"] += 1
            else:
                finalize_segment(current_segment)
                current_segment = {
                    "activity": activity_name,
                    "activity_source": point["_activity_source"],
                    "start_time": timestamp,
                    "end_time": minute_end,
                    "state_counts": defaultdict(int, {state: 1}),
                    "confidence_total": point["confidence"],
                    "points_count": 1,
                }

        finalize_segment(current_segment)

        logger.debug(
            "Generated %s activity segments between %s and %s",
            len(activities),
            start_time.isoformat(),
            end_time.isoformat(),
        )

        return activities
    
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
            
            # Make sure we don't go past end_time
            if hour_end > end_time:
                hour_end = end_time
            
            score = await self.get_cognitive_score(user_id, current, hour_end)
            
            if hour not in hourly_scores:
                hourly_scores[hour] = []
            hourly_scores[hour].append(score)
            
            current = hour_end
        
        # Average by hour
        avg_by_hour = {
            hour: sum(scores) / len(scores)
            for hour, scores in hourly_scores.items()
            if len(scores) > 0
        }
        
        # Find best hours
        if avg_by_hour:
            best_hours = sorted(avg_by_hour.items(), key=lambda x: x[1], reverse=True)[:3]
        else:
            best_hours = []
        
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
        
        total_focus_time = sum(w['duration'] for w in focus_windows)
        avg_duration = total_focus_time / len(focus_windows) if focus_windows else 0
        
        return {
            "pattern_type": "focus_windows",
            "windows": focus_windows,
            "total_focus_time": total_focus_time,
            "avg_window_duration": round(avg_duration, 1)
        }

    def _infer_activity_from_state(self, state: Optional[str]) -> str:
        """Infer a friendly activity label when none is provided."""

        state_activity_map = {
            "deep_focus": "focus_session",
            "creative_flow": "creative_work",
            "relaxed": "restorative_break",
            "stressed": "high_pressure_task",
            "drowsy": "fatigue_period",
            "distracted": "context_switching",
            "neutral": "light_tasking",
            "meditative_deep": "meditation",
            "unknown": "unspecified_activity",
        }

        return state_activity_map.get(state or "unknown", "unspecified_activity")
    
    def _aggregate_data(
        self,
        data_points: List[Dict[str, Any]],
        granularity: str
    ) -> List[Dict[str, Any]]:
        """
        Aggregate data points by granularity
        """
        
        if granularity == "minute" or not data_points:
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
