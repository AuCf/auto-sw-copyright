from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import settings, blueprint, code, manual, form_info, export
import os
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse, JSONResponse

app = FastAPI(
    title="AutoCopyright-AI Backend",
    description="AI-powered Chinese Software Copyright Material Generator API",
    version="1.0.0"
)

# Enable CORS
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
DIST_CANDIDATES = [
    Path(__file__).resolve().parent.parent.parent / "frontend" / "dist",
    Path(__file__).resolve().parent.parent / "frontend" / "dist",
    Path(__file__).resolve().parent.parent / "static",
    Path("/app/frontend/dist"),
]

ACTIVE_DIST_DIR: Path | None = None
for candidate in DIST_CANDIDATES:
    if candidate.exists() and (candidate / "index.html").exists():
        ACTIVE_DIST_DIR = candidate
        break

if ACTIVE_DIST_DIR:
    assets_dir = ACTIVE_DIST_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        if not ACTIVE_DIST_DIR:
            return JSONResponse({"error": "Frontend dist not found"}, status_code=404)
        file_path = ACTIVE_DIST_DIR / full_path
        if file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(ACTIVE_DIST_DIR / "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "system": "AutoCopyright-AI Backend",
            "status": "online",
            "version": "1.0.0",
            "api_docs": "/docs",
            "note": "Frontend dist not mounted. Visit /docs to test API."
        }
