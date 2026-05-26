import os
from backend.config import settings

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    firebase_admin = None
    credentials = None
    firestore = None

db = None
is_mock = True

if settings.is_firebase_configured and firebase_admin:
    try:
        # Format the private key to handle newline characters properly
        private_key = settings.FIREBASE_PRIVATE_KEY.replace('\\n', '\n')
        if not private_key.startswith("-----BEGIN PRIVATE KEY-----"):
            # Ensure it is wrapped correctly if quotes or formatting is slightly off
            pass

        cred_dict = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key": private_key,
            "client_email": settings.FIREBASE_CLIENT_EMAIL,
            "token_uri": "https://oauth2.googleapis.com/token",
        }

        # Check if already initialized to avoid duplicate initialization errors in reload
        if not firebase_admin._apps:
            cred = credentials.Certificate(cred_dict)
            firebase_admin.initialize_app(cred)
        
        db = firestore.client()
        is_mock = False
        print("Firebase Admin SDK successfully initialized with Cloud Firestore.")
    except Exception as e:
        print(f"Failed to initialize Firebase Admin: {e}. SecureRepo will run in local Mock DB mode.")
        db = None
        is_mock = True
else:
    print("Firebase environment variables are missing or placeholder. Running in local Mock DB mode.")
    db = None
    is_mock = True
