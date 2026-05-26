import os
from dotenv import load_dotenv

# Load .env file from backend directory or root directory
load_dotenv()

class Settings:
    PORT: int = int(os.getenv("PORT", 8000))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    
    # GitHub Service
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN", "")
    
    # Gemini Configuration
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    
    # Firebase Admin SDK configuration
    FIREBASE_PROJECT_ID: str = os.getenv("FIREBASE_PROJECT_ID", "")
    FIREBASE_CLIENT_EMAIL: str = os.getenv("FIREBASE_CLIENT_EMAIL", "")
    FIREBASE_PRIVATE_KEY: str = os.getenv("FIREBASE_PRIVATE_KEY", "")
    
    # Frontend URL for CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    @property
    def is_gemini_configured(self) -> bool:
        return bool(self.GEMINI_API_KEY and self.GEMINI_API_KEY != "your_gemini_api_key")

    @property
    def is_firebase_configured(self) -> bool:
        # Check if basic firestore configurations are available and not placeholder text
        has_project_id = bool(self.FIREBASE_PROJECT_ID and "your_project_id" not in self.FIREBASE_PROJECT_ID)
        has_client_email = bool(self.FIREBASE_CLIENT_EMAIL and "your_service_account_email" not in self.FIREBASE_CLIENT_EMAIL)
        has_private_key = bool(self.FIREBASE_PRIVATE_KEY and "your_private_key" not in self.FIREBASE_PRIVATE_KEY)
        return has_project_id and has_client_email and has_private_key

settings = Settings()
