from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import get_settings
from app.api.routes import chat, data, insights, user
import os
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

# Ensure Uvicorn doesn't reset our level back to INFO after startup
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)
for handler in root_logger.handlers:
    handler.setLevel(logging.DEBUG)

# Explicitly bump our app namespaces in case propagation is altered
logging.getLogger("app").setLevel(logging.DEBUG)
logging.getLogger("app.services").setLevel(logging.DEBUG)
logging.getLogger("app.api").setLevel(logging.DEBUG)


settings = get_settings()

app = FastAPI(
    title=settings.APP_NAME,
    description="LLM-powered brain data intelligence platform",
    version="0.1.0",
    debug=settings.DEBUG
)

# CORS - Allow Railway frontend
allowed_origins = settings.CORS_ORIGINS.copy()
allow_origin_regex = None

if settings.ENVIRONMENT == "production":
    frontend_url = os.getenv("FRONTEND_URL")
    if frontend_url:
        allowed_origins.append(frontend_url.rstrip("/"))

    railway_public_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN") or os.getenv("RAILWAY_URL")
    if railway_public_domain:
        sanitized = railway_public_domain.rstrip("/")
        if not sanitized.startswith("http"):
            sanitized = f"https://{sanitized}"
        allowed_origins.append(sanitized)

    allow_origin_regex = r"^https://([a-zA-Z0-9-]+\.)?railway\.app$"
else:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=allow_origin_regex,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
app.include_router(data.router, prefix="/api/data", tags=["data"])
app.include_router(insights.router, prefix="/api/insights", tags=["insights"])
app.include_router(user.router, prefix="/api/user", tags=["user"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": settings.APP_NAME,
        "version": "0.1.0",
        "status": "running"
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}
