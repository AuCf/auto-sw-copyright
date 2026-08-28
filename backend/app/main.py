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

@app.get("/api/health")
def health():
    return {"status": "healthy"}

# Single-Process Serving: Serve built Vue 3 frontend if dist directory exists
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse

DIST_DIR = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if not DIST_DIR.exists():
    # Check alternate location inside backend/static
    DIST_DIR = Path(__file__).resolve().parent.parent / "static"

if DIST_DIR.exists():
    app.mount("/assets", StaticFiles(directory=str(DIST_DIR / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = DIST_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(DIST_DIR / "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "system": "AutoCopyright-AI Backend",
            "status": "online",
            "version": "1.0.0",
            "note": "Frontend dist not found. Run Vite dev server or build frontend dist."
        }

