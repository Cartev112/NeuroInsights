"""Brain wave patterns and cognitive state definitions"""

# Frequency bands (Hz)
FREQUENCY_BANDS = {
    'delta': (0.5, 4),    # Deep sleep, unconscious
    'theta': (4, 8),      # Drowsiness, meditation, creativity
    'alpha': (8, 13),     # Relaxed, calm, not thinking
    'beta': (13, 30),     # Alert, focused, active thinking
    'gamma': (30, 100)    # High-level cognition, peak focus
}

# Cognitive state definitions
# Values: 'very_low' (0-0.2), 'low' (0.2-0.4), 'moderate' (0.4-0.6), 'high' (0.6-0.8), 'very_high' (0.8-1.0)
COGNITIVE_STATES = {
    'deep_focus': {
        'delta': 0.1,
        'theta': 0.2,
        'alpha': 0.15,
        'beta': 0.75,
        'gamma': 0.55,
        'description': 'Intense concentration on task',
        'typical_duration': (30, 120),  # minutes
    },
    'relaxed': {
        'delta': 0.15,
        'theta': 0.4,
        'alpha': 0.8,
        'beta': 0.25,
        'gamma': 0.2,
        'description': 'Calm, awake, not actively thinking',
        'typical_duration': (10, 60),
    },
    'stressed': {
        'delta': 0.1,
        'theta': 0.15,
        'alpha': 0.1,
        'beta': 0.9,
        'gamma': 0.4,
        'description': 'Anxious, overwhelmed',
        'typical_duration': (5, 30),
    },
    'creative_flow': {
        'delta': 0.15,
        'theta': 0.7,
        'alpha': 0.65,
        'beta': 0.45,
        'gamma': 0.5,
        'description': 'Creative thinking, idea generation',
        'typical_duration': (20, 90),
    },
    'drowsy': {
        'delta': 0.4,
        'theta': 0.75,
        'alpha': 0.45,
        'beta': 0.2,
        'gamma': 0.15,
        'description': 'Tired, low alertness',
        'typical_duration': (10, 45),
    },
    'distracted': {
        'delta': 0.2,
        'theta': 0.35,
        'alpha': 0.4,
        'beta': 0.5,
        'gamma': 0.3,
        'description': 'Attention wandering',
        'typical_duration': (5, 20),
        'fluctuation': True,  # Add noise/variability
    },
    'neutral': {
        'delta': 0.25,
        'theta': 0.35,
        'alpha': 0.45,
        'beta': 0.4,
        'gamma': 0.3,
        'description': 'Baseline state',
        'typical_duration': (5, 30),
    },
    'meditative_deep': {
        'delta': 0.3,
        'theta': 0.8,
        'alpha': 0.75,
        'beta': 0.15,
        'gamma': 0.25,
        'description': 'Deep meditation state',
        'typical_duration': (10, 30),
    }
}

# Activity categories and their typical states
ACTIVITY_STATE_MAPPING = {
    'coding': ['deep_focus', 'focused', 'distracted'],
    'writing': ['creative_flow', 'focused', 'distracted'],
    'meeting': ['focused', 'neutral', 'stressed'],
    'email': ['neutral', 'focused', 'distracted'],
    'break': ['relaxed', 'neutral'],
    'meditation': ['relaxed', 'meditative_deep'],
    'brainstorming': ['creative_flow', 'focused'],
    'reading': ['focused', 'relaxed', 'drowsy'],
    'exercise': ['focused', 'stressed'],
}

# Pre-built scenarios
SCENARIOS = {
    'typical_workday': {
        'duration': 480,  # 8 hours in minutes
        'timeline': [
            {'time': 0, 'state': 'neutral', 'activity': 'morning_emails', 'duration': 20},
            {'time': 20, 'state': 'deep_focus', 'activity': 'coding', 'duration': 90},
            {'time': 110, 'state': 'distracted', 'activity': 'coding', 'duration': 10},
            {'time': 120, 'state': 'relaxed', 'activity': 'break', 'duration': 15},
            {'time': 135, 'state': 'neutral', 'activity': 'meeting', 'duration': 60},
            {'time': 195, 'state': 'relaxed', 'activity': 'lunch', 'duration': 45},
            {'time': 240, 'state': 'deep_focus', 'activity': 'coding', 'duration': 75},
            {'time': 315, 'state': 'distracted', 'activity': 'coding', 'duration': 15},
            {'time': 330, 'state': 'neutral', 'activity': 'email', 'duration': 30},
            {'time': 360, 'state': 'creative_flow', 'activity': 'brainstorming', 'duration': 45},
            {'time': 405, 'state': 'neutral', 'activity': 'wrap_up', 'duration': 30},
            {'time': 435, 'state': 'drowsy', 'activity': 'email', 'duration': 45},
        ]
    },
    'meditation_session': {
        'duration': 20,
        'timeline': [
            {'time': 0, 'state': 'stressed', 'activity': 'meditation', 'duration': 3},
            {'time': 3, 'state': 'neutral', 'activity': 'meditation', 'duration': 2},
            {'time': 5, 'state': 'relaxed', 'activity': 'meditation', 'duration': 5},
            {'time': 10, 'state': 'meditative_deep', 'activity': 'meditation', 'duration': 8},
            {'time': 18, 'state': 'relaxed', 'activity': 'meditation', 'duration': 2}
        ]
    },
    'creative_work': {
        'duration': 120,
        'timeline': [
            {'time': 0, 'state': 'neutral', 'activity': 'brainstorming', 'duration': 15},
            {'time': 15, 'state': 'creative_flow', 'activity': 'writing', 'duration': 45},
            {'time': 60, 'state': 'distracted', 'activity': 'writing', 'duration': 10},
            {'time': 70, 'state': 'relaxed', 'activity': 'break', 'duration': 10},
            {'time': 80, 'state': 'creative_flow', 'activity': 'writing', 'duration': 40}
        ]
    },
    'stressful_day': {
        'duration': 480,
        'timeline': [
            {'time': 0, 'state': 'stressed', 'activity': 'urgent_email', 'duration': 30},
            {'time': 30, 'state': 'stressed', 'activity': 'meeting', 'duration': 60},
            {'time': 90, 'state': 'stressed', 'activity': 'problem_solving', 'duration': 90},
            {'time': 180, 'state': 'neutral', 'activity': 'lunch', 'duration': 20},
            {'time': 200, 'state': 'stressed', 'activity': 'coding', 'duration': 120},
            {'time': 320, 'state': 'distracted', 'activity': 'coding', 'duration': 30},
            {'time': 350, 'state': 'stressed', 'activity': 'meeting', 'duration': 60},
            {'time': 410, 'state': 'drowsy', 'activity': 'email', 'duration': 70},
        ]
    },
    'productive_morning': {
        'duration': 180,
        'timeline': [
            {'time': 0, 'state': 'neutral', 'activity': 'planning', 'duration': 15},
            {'time': 15, 'state': 'deep_focus', 'activity': 'coding', 'duration': 90},
            {'time': 105, 'state': 'relaxed', 'activity': 'break', 'duration': 15},
            {'time': 120, 'state': 'deep_focus', 'activity': 'coding', 'duration': 60},
        ]
    }
}
