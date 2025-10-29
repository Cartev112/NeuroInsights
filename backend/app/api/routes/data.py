"""Brain data API routes"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional
from datetime import datetime
from uuid import UUID
import logging

from app.models.schemas import (
    BrainDataPointResponse,
    BrainSessionResponse,
    StateDistribution,
    CognitiveScore
)
from app.services.data_service import get_data_service

router = APIRouter()
logger = logging.getLogger(__name__)

# Mock user ID for MVP
MOCK_USER_ID = UUID('12345678-1234-5678-1234-567812345678')


@router.get("/brain-waves")
async def get_brain_waves(
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    granularity: str = Query("5min"),
    data_service = Depends(get_data_service)
):
    """Get brain wave data for a time range"""
    
    try:
        logger.debug(
            "API /brain-waves request",
            extra={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "granularity": granularity,
            },
        )

        data = await data_service.get_brain_data(
            MOCK_USER_ID,
            start_time,
            end_time,
            granularity
        )
        logger.debug("Returning %s brain wave points", len(data))
        
        return {
            "start_time": start_time,
            "end_time": end_time,
            "granularity": granularity,
            "data_points": data
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/state-distribution", response_model=StateDistribution)
async def get_state_distribution(
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    data_service = Depends(get_data_service)
):
    """Get cognitive state distribution"""
    
    try:
        logger.debug(
            "API /state-distribution request",
            extra={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            },
        )

        distribution = await data_service.get_state_distribution(
            MOCK_USER_ID,
            start_time,
            end_time
        )
        logger.debug("State distribution payload: %s", distribution.model_dump())
        
        return distribution
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cognitive-score")
async def get_cognitive_score(
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    data_service = Depends(get_data_service)
):
    """Get cognitive fitness score"""
    
    try:
        logger.debug(
            "API /cognitive-score request",
            extra={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            },
        )

        score = await data_service.get_cognitive_score(
            MOCK_USER_ID,
            start_time,
            end_time
        )
        logger.debug("Cognitive score response: %s", score)
        
        return {
            "start_time": start_time,
            "end_time": end_time,
            "cognitive_score": score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/patterns")
async def find_patterns(
    pattern_type: str = Query(...),
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    activity: Optional[str] = Query(None),
    data_service = Depends(get_data_service)
):
    """Find patterns in brain data"""
    
    try:
        logger.debug(
            "API /patterns request",
            extra={
                "pattern_type": pattern_type,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "activity": activity,
            },
        )

        patterns = await data_service.find_patterns(
            MOCK_USER_ID,
            pattern_type,
            start_time,
            end_time,
            activity
        )
        logger.debug("Patterns result keys: %s", list(patterns.keys()) if isinstance(patterns, dict) else type(patterns))
        
        return patterns
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/activities")
async def get_activities(
    start_time: datetime = Query(...),
    end_time: datetime = Query(...),
    min_duration: int = Query(5, ge=1),
    data_service = Depends(get_data_service)
):
    """Get activity timeline for a period"""

    try:
        logger.debug(
            "API /activities request",
            extra={
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "min_duration": min_duration,
            },
        )

        activities = await data_service.get_activities(
            MOCK_USER_ID,
            start_time,
            end_time,
            min_duration_minutes=min_duration
        )

        return {
            "start_time": start_time,
            "end_time": end_time,
            "activities": activities
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
