from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from routes.scan_routes import router as scan_router

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent
FRONTEND_DIR = PROJECT_DIR / "frontend"

app = FastAPI(
    title="SecureRepo API",
    description="Student-friendly repository security scanner.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(scan_router, prefix="/api", tags=["Scan"])


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "SecureRepo"}


if FRONTEND_DIR.exists():
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIR), name="frontend-assets")

    @app.get("/", include_in_schema=False)
    def serve_homepage():
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/{path:path}", include_in_schema=False)
    def serve_static_frontend(path: str):
        target = FRONTEND_DIR / path
        if target.is_file():
            return FileResponse(target)
        return FileResponse(FRONTEND_DIR / "index.html")
