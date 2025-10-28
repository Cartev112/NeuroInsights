"""Mock brain data generators"""

import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple
from uuid import UUID
import random

from app.core.mock_data.patterns import COGNITIVE_STATES, SCENARIOS, FREQUENCY_BANDS


class MockBrainDataGenerator:
    """Generates realistic mock EEG data"""
    
    def __init__(self, user_id: UUID, seed: Optional[int] = None):
        self.user_id = user_id
        self.seed = seed or int(str(user_id)[:8], 16)
        self.rng = np.random.default_rng(self.seed)
        
        # User-specific baseline variations (±10%)
        self.baseline_variation = {
            'delta': self.rng.uniform(0.9, 1.1),
            'theta': self.rng.uniform(0.9, 1.1),
            'alpha': self.rng.uniform(0.9, 1.1),
            'beta': self.rng.uniform(0.9, 1.1),
            'gamma': self.rng.uniform(0.9, 1.1),
        }
        
        self.noise_level = 0.15  # 15% noise
    
    def generate_session_from_scenario(
        self,
        scenario_name: str,
        start_time: datetime
    ) -> Dict[str, Any]:
        """Generate a complete session from a pre-built scenario"""
        
        if scenario_name not in SCENARIOS:
            raise ValueError(f"Unknown scenario: {scenario_name}")
        
        scenario = SCENARIOS[scenario_name]
        duration_minutes = scenario['duration']
        timeline = scenario['timeline']
        
        # Generate data points (one per minute)
        data_points = []
        current_time = start_time
        
        for minute in range(duration_minutes):
            # Find which timeline segment we're in
            segment = self._get_timeline_segment(minute, timeline)
            state = segment['state']
            activity = segment.get('activity', 'unknown')
            
            # Generate brain wave data for this state
            brain_data = self._generate_state_data(state)
            
            data_points.append({
                'time': current_time,
                'delta': brain_data['delta'],
                'theta': brain_data['theta'],
                'alpha': brain_data['alpha'],
                'beta': brain_data['beta'],
                'gamma': brain_data['gamma'],
                'state': state,
                'activity': activity,
                'confidence': self._calculate_confidence(brain_data, state)
            })
            
            current_time += timedelta(minutes=1)
        
        return {
            'start_time': start_time,
            'end_time': start_time + timedelta(minutes=duration_minutes),
            'duration_minutes': duration_minutes,
            'data_points': data_points,
            'scenario': scenario_name,
            'activities': self._extract_activities(timeline, start_time)
        }
    
    def generate_custom_session(
        self,
        duration_minutes: int,
        primary_state: str,
        start_time: datetime,
        include_transitions: bool = True
    ) -> Dict[str, Any]:
        """Generate a custom session with specified parameters"""
        
        if primary_state not in COGNITIVE_STATES:
            raise ValueError(f"Unknown state: {primary_state}")
        
        data_points = []
        current_time = start_time
        current_state = primary_state
        
        for minute in range(duration_minutes):
            # Occasionally transition to related states
            if include_transitions and minute > 0 and self.rng.random() < 0.05:
                current_state = self._get_transition_state(current_state)
            
            brain_data = self._generate_state_data(current_state)
            
            data_points.append({
                'time': current_time,
                'delta': brain_data['delta'],
                'theta': brain_data['theta'],
                'alpha': brain_data['alpha'],
                'beta': brain_data['beta'],
                'gamma': brain_data['gamma'],
                'state': current_state,
                'confidence': self._calculate_confidence(brain_data, current_state)
            })
            
            current_time += timedelta(minutes=1)
        
        return {
            'start_time': start_time,
            'end_time': start_time + timedelta(minutes=duration_minutes),
            'duration_minutes': duration_minutes,
            'data_points': data_points,
            'primary_state': primary_state
        }
    
    def _generate_state_data(self, state: str) -> Dict[str, float]:
        """Generate brain wave data for a specific cognitive state"""
        
        state_pattern = COGNITIVE_STATES[state]
        
        # Base values from pattern
        base_values = {
            'delta': state_pattern['delta'],
            'theta': state_pattern['theta'],
            'alpha': state_pattern['alpha'],
            'beta': state_pattern['beta'],
            'gamma': state_pattern['gamma'],
        }
        
        # Apply user-specific baseline variation
        for band in base_values:
            base_values[band] *= self.baseline_variation[band]
        
        # Add noise
        noisy_values = {}
        for band, value in base_values.items():
            noise = self.rng.normal(0, self.noise_level * value)
            noisy_values[band] = max(0.0, min(1.0, value + noise))
        
        # Add extra fluctuation for distracted state
        if state_pattern.get('fluctuation', False):
            for band in noisy_values:
                extra_noise = self.rng.normal(0, 0.1)
                noisy_values[band] = max(0.0, min(1.0, noisy_values[band] + extra_noise))
        
        # Normalize to ensure realistic distribution
        total = sum(noisy_values.values())
        if total > 0:
            for band in noisy_values:
                noisy_values[band] = noisy_values[band] / total * len(noisy_values) * 0.4
        
        return noisy_values
    
    def _calculate_confidence(self, brain_data: Dict[str, float], expected_state: str) -> float:
        """Calculate confidence score for state detection"""
        
        state_pattern = COGNITIVE_STATES[expected_state]
        
        # Calculate how well the data matches the expected pattern
        differences = []
        for band in ['delta', 'theta', 'alpha', 'beta', 'gamma']:
            expected = state_pattern[band]
            actual = brain_data[band]
            diff = abs(expected - actual)
            differences.append(diff)
        
        avg_diff = np.mean(differences)
        confidence = max(0.5, 1.0 - avg_diff)
        
        return round(confidence, 2)
    
    def _get_timeline_segment(self, minute: int, timeline: List[Dict]) -> Dict:
        """Get the timeline segment for a given minute"""
        
        for i, segment in enumerate(timeline):
            segment_start = segment['time']
            segment_end = segment_start + segment['duration']
            
            if segment_start <= minute < segment_end:
                return segment
        
        # Return last segment if we're past the timeline
        return timeline[-1]
    
    def _extract_activities(
        self,
        timeline: List[Dict],
        start_time: datetime
    ) -> List[Dict[str, Any]]:
        """Extract activities from timeline"""
        
        activities = []
        for segment in timeline:
            if 'activity' in segment:
                activities.append({
                    'name': segment['activity'],
                    'start_time': start_time + timedelta(minutes=segment['time']),
                    'end_time': start_time + timedelta(minutes=segment['time'] + segment['duration']),
                    'duration': segment['duration']
                })
        
        return activities
    
    def _get_transition_state(self, current_state: str) -> str:
        """Get a likely transition state from current state"""
        
        # Define likely transitions
        transitions = {
            'deep_focus': ['neutral', 'distracted', 'stressed'],
            'relaxed': ['neutral', 'drowsy', 'creative_flow'],
            'stressed': ['neutral', 'distracted', 'deep_focus'],
            'creative_flow': ['relaxed', 'neutral', 'distracted'],
            'drowsy': ['neutral', 'relaxed'],
            'distracted': ['neutral', 'deep_focus', 'stressed'],
            'neutral': ['deep_focus', 'relaxed', 'distracted'],
        }
        
        possible_states = transitions.get(current_state, ['neutral'])
        return self.rng.choice(possible_states)
    
    def add_artifacts(self, data: np.ndarray) -> np.ndarray:
        """Add realistic artifacts (eye blinks, movement, etc.)"""
        
        # Randomly add spikes (artifacts)
        artifact_probability = 0.02  # 2% chance per data point
        
        for i in range(len(data)):
            if self.rng.random() < artifact_probability:
                # Add a spike
                spike_magnitude = self.rng.uniform(0.2, 0.5)
                data[i] = min(1.0, data[i] + spike_magnitude)
        
        return data


class MockDataProvider:
    """Provides mock brain data for users"""
    
    def __init__(self):
        self.generators: Dict[UUID, MockBrainDataGenerator] = {}
    
    def get_generator(self, user_id: UUID) -> MockBrainDataGenerator:
        """Get or create generator for user"""
        
        if user_id not in self.generators:
            self.generators[user_id] = MockBrainDataGenerator(user_id)
        
        return self.generators[user_id]
    
    def generate_historical_data(
        self,
        user_id: UUID,
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """Generate historical data for a user"""
        
        generator = self.get_generator(user_id)
        sessions = []
        
        # Generate data for each day
        end_date = datetime.now()
        
        for day in range(days):
            date = end_date - timedelta(days=days - day)
            
            # Skip weekends sometimes
            if date.weekday() >= 5 and random.random() < 0.3:
                continue
            
            # Generate 1-3 sessions per day
            num_sessions = random.randint(1, 3)
            
            for session_num in range(num_sessions):
                # Pick a random scenario
                scenario = random.choice(list(SCENARIOS.keys()))
                
                # Set start time (morning, afternoon, or evening)
                if session_num == 0:
                    hour = random.randint(8, 10)
                elif session_num == 1:
                    hour = random.randint(13, 15)
                else:
                    hour = random.randint(18, 20)
                
                start_time = date.replace(hour=hour, minute=0, second=0, microsecond=0)
                
                session_data = generator.generate_session_from_scenario(
                    scenario,
                    start_time
                )
                
                sessions.append(session_data)
        
        return sessions


# Singleton instance
mock_data_provider = MockDataProvider()
