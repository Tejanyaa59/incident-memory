import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database.session import Base, engine, SessionLocal
from app.seed.seeder import seed_database
from app.api import (
    health_router,
    dashboard_router,
    incidents_router,
    investigations_router,
    memory_router,
    learning_router,
    history_router,
    demo_router,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("incidentlens")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure tables exist and seed initial data if empty
    logger.info("[STARTUP] Initializing database and ensuring seed data...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_database(db=db)
    finally:
        db.close()
    logger.info("[STARTUP] IncidentLens backend is ready.")
    yield
    # Shutdown
    logger.info("[SHUTDOWN] IncidentLens backend shutting down.")

app = FastAPI(
    title="IncidentLens API",
    description="Learning-First AI Incident Investigator with real Hindsight memory integration.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.FRONTEND_ORIGINS if settings.FRONTEND_ORIGINS else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_router)
app.include_router(dashboard_router)
app.include_router(incidents_router)
app.include_router(investigations_router)
app.include_router(memory_router)
app.include_router(learning_router)
app.include_router(history_router)
app.include_router(demo_router)

@app.get("/", tags=["Health"])
def root():
    return {
        "name": "IncidentLens API",
        "tagline": "Don't investigate the same incident twice.",
        "status": "online",
        "docs": "/docs",
    }
