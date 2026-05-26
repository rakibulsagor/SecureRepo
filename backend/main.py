import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.routes import health_routes, scan_routes, report_routes, history_routes

app = FastAPI(
    title="SecureRepo API",
    description="Rule-based GitHub security scanner backend with student-friendly explanations.",
    version="1.0.0"
)

# Set up CORS middleware to allow communication from the React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers
app.include_router(health_routes.router, tags=["Health"])
app.include_router(scan_routes.router, tags=["Scanner"])
app.include_router(report_routes.router, tags=["Reports"])
app.include_router(history_routes.router, tags=["History"])

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
