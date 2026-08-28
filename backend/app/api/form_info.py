from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.core.llm import LLMService
from app.core.code_engine import CodeSynthesisEngine

router = APIRouter(prefix="/api/form-info", tags=["Application Form"])

class FormInfoRequest(BaseModel):
    software_name: str
    language: str
    features: Optional[str] = None

@router.post("/generate")
async def generate_form_info(req: FormInfoRequest):
    llm = LLMService()
    engine = CodeSynthesisEngine(llm)
    try:
        data = await engine.generate_form_info(
            software_name=req.software_name,
            language=req.language,
            features=req.features
        )
        return {"success": True, "form_info": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"申请表信息生成失败: {str(e)}")
