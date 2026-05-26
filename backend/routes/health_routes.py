from fastapi import APIRouter
from backend.firebase_admin_config import is_mock as firebase_mock
from backend.config import settings

router = APIRouter()

@router.get("/health")
def get_health():
    return {
        "status": "healthy",
        "firebase_mode": "mock" if firebase_mock else "cloud_firestore",
        "gemini_mode": "mock" if not settings.is_gemini_configured else "live_api"
    }
