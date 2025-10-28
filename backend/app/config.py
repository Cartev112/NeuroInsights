from pydantic_settings import BaseSettings
from functools import lru_cache
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # App
    APP_NAME: str = "NeuroInsights"
    ENVIRONMENT: str = os.getenv("RAILWAY_ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("RAILWAY_ENVIRONMENT") != "production"
    
    # Database (Railway provides DATABASE_URL automatically)
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://neuroinsights:neuroinsights_dev@localhost:5432/neuroinsights")
    
    # Redis (Railway provides REDIS_URL automatically)
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # OpenAI
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-4-turbo-preview"
    
    # JWT
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev_secret_change_in_production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    # CORS
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
