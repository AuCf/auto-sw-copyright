import base64
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional, List
from app.core.llm import LLMService
from app.core.code_engine import CodeSynthesisEngine
from app.core.ui_renderer import UIMockupRenderer

router = APIRouter(prefix="/api/manual", tags=["User Manual"])

class ChapterRequest(BaseModel):
    software_name: str
    version: str = "V1.0"
    chapter_title: str
    chapter_requirements: str

class FullManualRequest(BaseModel):
    software_name: str
    language: str
    blueprint: Dict[str, Any]

class MockupRequest(BaseModel):
    software_name: str
    version: str = "V1.0"
    modules: List[Dict[str, str]]

@router.post("/generate-chapter")
async def generate_chapter_endpoint(req: ChapterRequest):
    llm = LLMService()
    engine = CodeSynthesisEngine(llm)
    try:
        content = await engine.generate_manual_chapter(
            software_name=req.software_name,
            version=req.version,
            chapter_title=req.chapter_title,
            chapter_requirements=req.chapter_requirements
        )
        return {"success": True, "chapter_title": req.chapter_title, "content": content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"章节生成失败: {str(e)}")

@router.post("/generate-full-pipeline")
async def generate_full_manual_pipeline_endpoint(req: FullManualRequest):
    llm = LLMService()
    engine = CodeSynthesisEngine(llm)
    try:
        result = await engine.generate_full_manual_pipeline(
            software_name=req.software_name,
            language=req.language,
            blueprint=req.blueprint
        )
        # Note: mockups_bytes not sent over JSON, only mockups_b64
        return {
            "success": True,
            "total_words": result["total_words"],
            "chapters": result["chapters"],
            "full_markdown": result["full_markdown"],
            "mockups_b64": result["mockups_b64"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"说明书长文流水线生成失败: {str(e)}")

@router.post("/mockups")
async def generate_mockups_endpoint(req: MockupRequest):
    try:
        renderer = UIMockupRenderer(req.software_name, req.version)
        images = renderer.generate_all_mockups(req.modules)
        b64_dict = {}
        for k, v in images.items():
            b64_dict[k] = f"data:image/png;base64,{base64.b64encode(v).decode('utf-8')}"
        return {"success": True, "mockups_b64": b64_dict}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"UI 截图生成失败: {str(e)}")
