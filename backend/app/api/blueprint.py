from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.llm import LLMService
from app.core.code_engine import CodeSynthesisEngine

router = APIRouter(prefix="/api/blueprint", tags=["Blueprint"])

class BlueprintRequest(BaseModel):
    software_name: str
    language: str = "Java"
    features: Optional[str] = None

@router.post("/generate")
async def generate_blueprint(req: BlueprintRequest):
    if not req.software_name.strip():
        raise HTTPException(status_code=400, detail="软件全称不能为空")
    
    llm = LLMService()
    engine = CodeSynthesisEngine(llm)
    try:
        blueprint = await engine.generate_blueprint(
            software_name=req.software_name,
            language=req.language,
            features=req.features
        )
        return {"success": True, "blueprint": blueprint}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"蓝图生成失败: {str(e)}")
