from app.api.health import router as health_router
from app.api.dashboard import router as dashboard_router
from app.api.incidents import router as incidents_router
from app.api.investigations import router as investigations_router
from app.api.memory import router as memory_router
from app.api.learning import router as learning_router
from app.api.history import router as history_router
from app.api.demo import router as demo_router

__all__ = [
    "health_router",
    "dashboard_router",
    "incidents_router",
    "investigations_router",
    "memory_router",
    "learning_router",
    "history_router",
    "demo_router",
]
