from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Dict, Any, List
from uuid import UUID


# User schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Brain data schemas
class BrainWaveData(BaseModel):
    delta: float
    theta: float
    alpha: float
    beta: float
    gamma: float


class BrainDataPointResponse(BaseModel):
    time: datetime
    delta: float
    theta: float
    alpha: float
    beta: float
    gamma: float
    state: Optional[str] = None
    confidence: Optional[float] = None
    
    class Config:
        from_attributes = True


class BrainSessionResponse(BaseModel):
    id: UUID
    user_id: UUID
    start_time: datetime
    end_time: datetime
    data_source: str
    metadata: Dict[str, Any] = {}
    
    class Config:
        from_attributes = True


class BrainDataQuery(BaseModel):
    start_time: datetime
    end_time: datetime
    granularity: str = "minute"  # minute, 5min, hour


# Activity schemas
class ActivityCreate(BaseModel):
    name: str
    start_time: datetime
    end_time: datetime
    category: Optional[str] = None
    metadata: Dict[str, Any] = {}


class ActivityResponse(BaseModel):
    id: UUID
    user_id: UUID
    name: str
    start_time: datetime
    end_time: datetime
    category: Optional[str] = None
    
    class Config:
        from_attributes = True


# Chat schemas
class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    response: str
    metadata: Optional[Dict[str, Any]] = None


class ChatMessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Insight schemas
class InsightResponse(BaseModel):
    id: UUID
    insight_type: str
    content: str
    generated_at: datetime
    dismissed: bool = False
    
    class Config:
        from_attributes = True


# Analysis schemas
class CognitiveState(BaseModel):
    state: str
    confidence: float
    timestamp: datetime


class StateDistribution(BaseModel):
    deep_focus: float
    relaxed: float
    stressed: float
    creative_flow: float
    drowsy: float
    distracted: float
    neutral: float


class CognitiveScore(BaseModel):
    score: int = Field(..., ge=0, le=100)
    focus_time: float
    stress_level: float
    state_variability: float
    timestamp: datetime


class PatternCorrelation(BaseModel):
    activity: str
    state: str
    correlation_strength: float
    occurrences: int


class DailySummary(BaseModel):
    date: datetime
    cognitive_score: int
    focus_time: float
    stress_periods: int
    state_distribution: StateDistribution
    top_activities: List[str]
    insights: List[str]
