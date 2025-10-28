"""Insights API routes"""

from fastapi import APIRouter, HTTPException, Depends
from typing import List
from datetime import datetime, timedelta
from uuid import UUID

from app.models.schemas import InsightResponse
from app.services.llm_service import get_llm_service
from app.services.data_service import get_data_service

router = APIRouter()

# Mock user ID for MVP
MOCK_USER_ID = UUID('12345678-1234-5678-1234-567812345678')


@router.get("/daily")
async def get_daily_insights(
    date: str = None,
    llm_service = Depends(get_llm_service),
    data_service = Depends(get_data_service)
):
    """Get daily insights"""
    
    try:
        # Parse date or use today
        if date:
            target_date = datetime.fromisoformat(date)
        else:
            target_date = datetime.now()
        
        # Get data for the day
        start_time = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(days=1)
        
        # Get metrics
        distribution = await data_service.get_state_distribution(
            MOCK_USER_ID, start_time, end_time
        )
        
        score = await data_service.get_cognitive_score(
            MOCK_USER_ID, start_time, end_time
        )
        
        # Prepare data summary
        data_summary = {
            "date": target_date.date().isoformat(),
            "cognitive_score": score,
            "state_distribution": distribution.model_dump(),
            "focus_time": distribution.deep_focus + distribution.creative_flow,
            "stress_level": distribution.stressed
        }
        
        # Generate insights
        summary = await llm_service.generate_daily_summary(
            target_date.date().isoformat(),
            data_summary
        )
        
        return {
            "date": target_date.date().isoformat(),
            "summary": summary,
            "metrics": data_summary
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/generate")
async def generate_insight(
    llm_service = Depends(get_llm_service),
    data_service = Depends(get_data_service)
):
    """Generate a new insight from recent data"""
    
    try:
        # Get last 7 days of data
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        
        distribution = await data_service.get_state_distribution(
            MOCK_USER_ID, start_time, end_time
        )
        
        score = await data_service.get_cognitive_score(
            MOCK_USER_ID, start_time, end_time
        )
        
        data_summary = {
            "period": "last 7 days",
            "cognitive_score": score,
            "state_distribution": distribution.model_dump()
        }
        
        insight = await llm_service.generate_insight(data_summary)
        
        return {
            "insight": insight,
            "generated_at": datetime.now().isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
