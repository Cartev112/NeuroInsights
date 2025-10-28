"""User API routes"""

from fastapi import APIRouter, HTTPException
from uuid import UUID

router = APIRouter()

# Mock user ID for MVP
MOCK_USER_ID = UUID('12345678-1234-5678-1234-567812345678')


@router.get("/me")
async def get_current_user():
    """Get current user info (mock for MVP)"""
    
    return {
        "id": str(MOCK_USER_ID),
        "email": "demo@neuroinsights.com",
        "created_at": "2024-01-01T00:00:00Z"
    }


@router.get("/baseline")
async def get_user_baseline():
    """Get user's baseline brain patterns"""
    
    # TODO: Implement actual baseline calculation
    return {
        "user_id": str(MOCK_USER_ID),
        "avg_focus_time": 180,  # minutes
        "avg_stress_level": 0.3,
        "state_distribution": {
            "deep_focus": 25.0,
            "relaxed": 20.0,
            "stressed": 15.0,
            "creative_flow": 15.0,
            "drowsy": 10.0,
            "distracted": 10.0,
            "neutral": 5.0
        },
        "last_updated": "2024-01-01T00:00:00Z"
    }
