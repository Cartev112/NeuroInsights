from sqlalchemy import Column, String, DateTime, Float, Boolean, ForeignKey, Text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
import uuid

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class BrainSession(Base):
    __tablename__ = "brain_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    data_source = Column(String(50), default="mock")
    metadata = Column(JSONB, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class BrainDataPoint(Base):
    __tablename__ = "brain_data_points"
    
    time = Column(DateTime(timezone=True), primary_key=True, nullable=False, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("brain_sessions.id"), primary_key=True, nullable=False)
    delta = Column(Float)
    theta = Column(Float)
    alpha = Column(Float)
    beta = Column(Float)
    gamma = Column(Float)
    state = Column(String(50))
    confidence = Column(Float)


class Activity(Base):
    __tablename__ = "activities"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    session_id = Column(UUID(as_uuid=True), ForeignKey("brain_sessions.id"))
    name = Column(String(255), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=False, index=True)
    end_time = Column(DateTime(timezone=True), nullable=False)
    category = Column(String(100))
    metadata = Column(JSONB, default={})


class Insight(Base):
    __tablename__ = "insights"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    generated_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    insight_type = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    data_references = Column(JSONB, default={})
    dismissed = Column(Boolean, default=False)
    metadata = Column(JSONB, default={})


class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)
    role = Column(String(20), nullable=False)  # 'user' or 'assistant'
    content = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    metadata = Column(JSONB, default={})


class UserBaseline(Base):
    __tablename__ = "user_baselines"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True, index=True)
    avg_focus_time = Column(Float)  # minutes per day
    avg_stress_level = Column(Float)  # 0-1 scale
    state_distribution = Column(JSONB, default={})  # percentage of time in each state
    optimal_times = Column(JSONB, default={})  # best times for different activities
    last_updated = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSONB, default={})
