"""Function tools for LLM to query brain data"""

from typing import List, Dict, Any

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_brain_data",
            "description": "Retrieve brain wave data for a specific time range. Returns time-series data with brain wave frequencies and detected cognitive states.",
            "parameters": {
                "type": "object",
                "properties": {
                    "start_time": {
                        "type": "string",
                        "description": "Start time in ISO format or relative time like '2 hours ago', 'today at 9am', 'yesterday'"
                    },
                    "end_time": {
                        "type": "string",
                        "description": "End time in ISO format or relative time like 'now', 'today at 5pm'"
                    },
                    "granularity": {
                        "type": "string",
                        "enum": ["minute", "5min", "15min", "hour"],
                        "description": "Data granularity - how to aggregate the data points",
                        "default": "5min"
                    }
                },
                "required": ["start_time", "end_time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_state_distribution",
            "description": "Get the distribution of cognitive states over a time period. Shows percentage of time spent in each state (focused, relaxed, stressed, etc.)",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_period": {
                        "type": "string",
                        "description": "Time period like 'today', 'yesterday', 'this week', 'last 7 days', 'this month'"
                    }
                },
                "required": ["time_period"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "compare_time_periods",
            "description": "Compare brain patterns between two different time periods. Useful for tracking progress or identifying changes.",
            "parameters": {
                "type": "object",
                "properties": {
                    "period1": {
                        "type": "string",
                        "description": "First time period (e.g., 'today', 'this week', 'last Monday')"
                    },
                    "period2": {
                        "type": "string",
                        "description": "Second time period to compare against (e.g., 'yesterday', 'last week', 'previous Monday')"
                    },
                    "metric": {
                        "type": "string",
                        "enum": ["focus_time", "stress_level", "state_distribution", "cognitive_score", "all"],
                        "description": "Which metric to compare",
                        "default": "all"
                    }
                },
                "required": ["period1", "period2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "find_patterns",
            "description": "Find patterns or correlations in brain data. Can identify activity correlations, optimal times, or state transitions.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern_type": {
                        "type": "string",
                        "enum": ["activity_correlation", "time_of_day", "state_transitions", "focus_windows"],
                        "description": "Type of pattern to search for"
                    },
                    "time_range": {
                        "type": "string",
                        "description": "Time range to analyze (e.g., 'last 7 days', 'last 30 days')",
                        "default": "last 7 days"
                    },
                    "activity": {
                        "type": "string",
                        "description": "Specific activity to analyze (optional, for activity_correlation pattern type)"
                    }
                },
                "required": ["pattern_type"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_cognitive_score",
            "description": "Get the overall cognitive fitness score (0-100) for a time period. Based on focus time, stress levels, and state balance.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_period": {
                        "type": "string",
                        "description": "Time period like 'today', 'yesterday', 'this week'"
                    }
                },
                "required": ["time_period"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_activities",
            "description": "Get list of activities during a time period with their associated brain states.",
            "parameters": {
                "type": "object",
                "properties": {
                    "time_period": {
                        "type": "string",
                        "description": "Time period like 'today', 'yesterday', 'this week'"
                    }
                },
                "required": ["time_period"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_baseline",
            "description": "Get the user's baseline brain patterns for comparison. Shows their typical patterns over the last 30 days.",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": []
            }
        }
    }
]


def get_tool_descriptions() -> List[str]:
    """Get human-readable descriptions of available tools"""
    descriptions = []
    for tool in TOOLS:
        func = tool["function"]
        descriptions.append(f"- {func['name']}: {func['description']}")
    return descriptions
