from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import settings, blueprint, code, manual, form_info, export

app = FastAPI(
    title="AutoCopyright-AI Backend",
    description="AI-powered Chinese Software Copyright Material Generator API",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(settings.router)
app.include_router(blueprint.router)
app.include_router(code.router)
app.include_router(manual.router)
app.include_router(form_info.router)
app.include_router(export.router)

@app.get("/")
def root():
    return {
        "system": "AutoCopyright-AI Backend",
        "status": "online",
        "version": "1.0.0"
    }

@app.get("/api/health")
def health():
    return {"status": "healthy"}
