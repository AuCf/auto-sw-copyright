from fastapi import APIRouter, HTTPException
from app.config import load_settings, save_settings, LLMSettings
from app.core.llm import LLMService

router = APIRouter(prefix="/api/settings", tags=["Settings"])

@router.get("", response_model=LLMSettings)
def get_settings():
    return load_settings()

@router.post("")
def update_settings(settings: LLMSettings):
    save_settings(settings)
    return {"success": True, "message": "配置已保存"}

@router.post("/test")
async def test_llm_connection(settings: LLMSettings):
    service = LLMService(settings)
    result = await service.test_connection()
    if not result.get("success"):
        raise HTTPException(status_code=400, detail=result.get("error", "连接失败"))
    return result
