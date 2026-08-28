import os
import json
from pathlib import Path
from pydantic import BaseModel

CONFIG_FILE = Path(__file__).resolve().parent.parent / "settings.json"

class LLMSettings(BaseModel):
    provider: str = "deepseek"  # "deepseek" | "openai" | "ollama" | "custom"
    api_key: str = ""
    base_url: str = "https://api.deepseek.com/v1"
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 4096

def load_settings() -> LLMSettings:
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return LLMSettings(**data)
        except Exception:
            pass
    
    # Defaults: fallback to env vars if available
    api_key = os.getenv("OPENAI_API_KEY", os.getenv("DEEPSEEK_API_KEY", ""))
    base_url = os.getenv("OPENAI_BASE_URL", "https://api.deepseek.com/v1")
    model = os.getenv("LLM_MODEL", "deepseek-chat")
    
    return LLMSettings(api_key=api_key, base_url=base_url, model=model)

def save_settings(settings: LLMSettings):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings.model_dump(), f, ensure_ascii=False, indent=2)
