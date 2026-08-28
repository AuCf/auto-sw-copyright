import json
import re
from typing import AsyncGenerator, Optional, Dict, Any, List
import httpx
from app.config import load_settings, LLMSettings

class LLMService:
    def __init__(self, settings: Optional[LLMSettings] = None):
        self.settings = settings or load_settings()

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json"
        }
        if self.settings.api_key:
            headers["Authorization"] = f"Bearer {self.settings.api_key}"
        return headers

    def _get_endpoint(self) -> str:
        base_url = self.settings.base_url.rstrip("/")
        if not base_url.endswith("/v1") and not base_url.endswith("/chat/completions"):
            # If user provided base URL like https://api.deepseek.com
            if "/v1" not in base_url:
                base_url = f"{base_url}/v1"
        if not base_url.endswith("/chat/completions"):
            return f"{base_url}/chat/completions"
        return base_url

    async def test_connection(self) -> Dict[str, Any]:
        """Test if the LLM API is reachable and key is valid."""
        endpoint = self._get_endpoint()
        headers = self._get_headers()
        payload = {
            "model": self.settings.model,
            "messages": [
                {"role": "user", "content": "ping"}
            ],
            "max_tokens": 10
        }
        
        async with httpx.AsyncClient(timeout=15.0) as client:
            try:
                response = await client.post(endpoint, headers=headers, json=payload)
                if response.status_code == 200:
                    return {"success": True, "message": "API 连接成功！"}
                else:
                    return {
                        "success": False,
                        "status_code": response.status_code,
                        "error": response.text
                    }
            except Exception as e:
                return {"success": False, "error": str(e)}

    async def chat(self, messages: List[Dict[str, str]], temperature: Optional[float] = None, max_tokens: Optional[int] = None) -> str:
        """Non-streaming chat completion."""
        endpoint = self._get_endpoint()
        headers = self._get_headers()
        payload = {
            "model": self.settings.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.settings.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.settings.max_tokens,
        }

        async with httpx.AsyncClient(timeout=180.0) as client:
            response = await client.post(endpoint, headers=headers, json=payload)
            if response.status_code != 200:
                raise RuntimeError(f"LLM API Error ({response.status_code}): {response.text}")
            
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def chat_stream(self, messages: List[Dict[str, str]], temperature: Optional[float] = None) -> AsyncGenerator[str, None]:
        """Streaming chat completion."""
        endpoint = self._get_endpoint()
        headers = self._get_headers()
        payload = {
            "model": self.settings.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else self.settings.temperature,
            "stream": True,
        }

        async with httpx.AsyncClient(timeout=240.0) as client:
            async with client.stream("POST", endpoint, headers=headers, json=payload) as response:
                if response.status_code != 200:
                    error_text = await response.aread()
                    raise RuntimeError(f"LLM API Error ({response.status_code}): {error_text.decode()}")

                async for line in response.aiter_lines():
                    line = line.strip()
                    if not line or not line.startswith("data:"):
                        continue
                    if line == "data: [DONE]":
                        break
                    
                    json_str = line[5:].strip()
                    try:
                        chunk = json.loads(json_str)
                        delta = chunk.get("choices", [{}])[0].get("delta", {})
                        content = delta.get("content", "")
                        if content:
                            yield content
                    except Exception:
                        continue

    @staticmethod
    def extract_json(text: str) -> Dict[str, Any]:
        """Safely extract JSON object from markdown or raw string."""
        text = text.strip()
        # Remove ```json and ```
        match = re.search(r"```(?:json)?\s*([\s\S]*?)\s*```", text)
        if match:
            text = match.group(1).strip()
        
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find first { and last }
            start = text.find("{")
            end = text.rfind("}")
            if start != -1 and end != -1:
                return json.loads(text[start:end+1])
            raise ValueError(f"无法从 LLM 返回的内容中解析 JSON: {text[:200]}...")
