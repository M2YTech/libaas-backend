from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os 

from app.routes.auth import router as auth_router
from app.routes.wardrobe import router as wardrobe_router
from app.components.ai.clip_insights import analyze_image

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Server startup and shutdown."""
    print("Starting LibaasAI Backend...")
    print("AI Insights: Using GPT-4o-mini (API) for image analysis.")
    print("Fashion Recommendations: Using lightweight rule-based engine.")
    print("Outfit Generator: Using GPT-4o-mini (API).")
    print("Server startup complete!")
    print("API docs available at: /docs")
    yield
    print("Shutting down...")

app = FastAPI(
    title="LibaasAI Backend",
    description="AI-powered wardrobe assistant API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(wardrobe_router)

@app.get("/")
async def root():
    return {
        "message": "Welcome to LibaasAI API",
        "docs": "/docs",
        "health": "ok"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "libaas-ai-backend"}

