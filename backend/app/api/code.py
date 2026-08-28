from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from app.core.llm import LLMService
from app.core.code_engine import CodeSynthesisEngine, sanitize_code_text

router = APIRouter(prefix="/api/code", tags=["Code Generation"])

class LayerCodeRequest(BaseModel):
    software_name: str
    language: str
    layer_name: str
    layer_display_name: str
    layer_files: List[str]
    layer_description: str
    system_summary: str

class FullCodeRequest(BaseModel):
    software_name: str
    language: str
    blueprint: Dict[str, Any]

@router.post("/generate-layer")
async def generate_layer_code(req: LayerCodeRequest):
    llm = LLMService()
    engine = CodeSynthesisEngine(llm)
    try:
        raw_code = await engine.generate_layer_code(
            software_name=req.software_name,
            language=req.language,
            layer_name=req.layer_name,
            layer_display_name=req.layer_display_name,
            layer_files=req.layer_files,
            layer_description=req.layer_description,
            system_summary=req.system_summary
        )
        clean_lines = sanitize_code_text(raw_code)
        return {
            "success": True,
            "layer_name": req.layer_name,
            "display_name": req.layer_display_name,
            "lines_count": len(clean_lines),
            "code": "\n".join(clean_lines)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"生成层代码失败: {str(e)}")

@router.post("/generate-full")
async def generate_full_code(req: FullCodeRequest):
    llm = LLMService()
    engine = CodeSynthesisEngine(llm)
    try:
        result = await engine.generate_full_pipeline(
            software_name=req.software_name,
            language=req.language,
            blueprint=req.blueprint
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"全量代码生成失败: {str(e)}")
