"""
Клиент для работы с Ollama API
"""

import asyncio
import aiohttp
import json
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
import logging

logger = logging.getLogger(__name__)

class OllamaGenerateRequest(BaseModel):
    model: str
    prompt: str
    stream: bool = False
    options: Optional[Dict[str, Any]] = None
    system: Optional[str] = None
    template: Optional[str] = None
    context: Optional[List[int]] = None
    raw: Optional[bool] = None
    format: Optional[str] = None

class OllamaGenerateResponse(BaseModel):
    model: str
    created_at: str
    response: str
    done: bool
    context: Optional[List[int]] = None
    total_duration: Optional[int] = None
    load_duration: Optional[int] = None
    prompt_eval_count: Optional[int] = None
    prompt_eval_duration: Optional[int] = None
    eval_count: Optional[int] = None
    eval_duration: Optional[int] = None

class OllamaModelInfo(BaseModel):
    name: str
    modified_at: str
    size: int
    digest: str
    details: Optional[Dict[str, Any]] = None

class OllamaClient:
    """Клиент для работы с Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')
        self.session: Optional[aiohttp.ClientSession] = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Выполнить HTTP запрос к Ollama API"""
        if not self.session:
            raise RuntimeError("Сессия не инициализирована. Используйте async with OllamaClient() as client:")
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            async with self.session.request(method, url, json=data) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"Ошибка API: {response.status} - {error_text}")
                    raise Exception(f"Ошибка API: {response.status} - {error_text}")
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка подключения к Ollama: {e}")
            raise Exception(f"Не удается подключиться к Ollama API: {e}")
    
    async def health_check(self) -> bool:
        """Проверить доступность Ollama API"""
        try:
            await self._make_request("GET", "/api/tags")
            return True
        except Exception:
            return False
    
    async def list_models(self) -> List[OllamaModelInfo]:
        """Получить список доступных моделей"""
        response = await self._make_request("GET", "/api/tags")
        models = []
        for model_data in response.get("models", []):
            models.append(OllamaModelInfo(**model_data))
        return models
    
    async def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Загрузить модель"""
        data = {"name": model_name}
        return await self._make_request("POST", "/api/pull", data)
    
    async def generate(self, request: OllamaGenerateRequest) -> OllamaGenerateResponse:
        """Сгенерировать ответ от модели"""
        response_data = await self._make_request("POST", "/api/generate", request.dict())
        return OllamaGenerateResponse(**response_data)
    
    async def generate_stream(self, request: OllamaGenerateRequest):
        """Сгенерировать ответ от модели в потоковом режиме"""
        if not self.session:
            raise RuntimeError("Сессия не инициализирована")
        
        url = f"{self.base_url}/api/generate"
        
        async with self.session.post(url, json=request.dict()) as response:
            if response.status != 200:
                error_text = await response.text()
                raise Exception(f"Ошибка API: {response.status} - {error_text}")
            
            async for line in response.content:
                if line:
                    try:
                        data = json.loads(line.decode('utf-8'))
                        yield OllamaGenerateResponse(**data)
                    except json.JSONDecodeError:
                        continue
    
    async def chat(self, model: str, messages: List[Dict[str, str]], stream: bool = False) -> Dict[str, Any]:
        """Чат с моделью"""
        data = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        return await self._make_request("POST", "/api/chat", data)
    
    async def embeddings(self, model: str, prompt: str) -> Dict[str, Any]:
        """Получить эмбеддинги для текста"""
        data = {
            "model": model,
            "prompt": prompt
        }
        return await self._make_request("POST", "/api/embeddings", data)

# Синхронная обертка для удобства использования
class OllamaClientSync:
    """Синхронная обертка для OllamaClient"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
    
    def health_check(self) -> bool:
        """Проверить доступность Ollama API"""
        return asyncio.run(self._async_health_check())
    
    async def _async_health_check(self) -> bool:
        async with OllamaClient(self.base_url) as client:
            return await client.health_check()
    
    def list_models(self) -> List[OllamaModelInfo]:
        """Получить список доступных моделей"""
        return asyncio.run(self._async_list_models())
    
    async def _async_list_models(self) -> List[OllamaModelInfo]:
        async with OllamaClient(self.base_url) as client:
            return await client.list_models()
    
    def generate(self, request: OllamaGenerateRequest) -> OllamaGenerateResponse:
        """Сгенерировать ответ от модели"""
        return asyncio.run(self._async_generate(request))
    
    async def _async_generate(self, request: OllamaGenerateRequest) -> OllamaGenerateResponse:
        async with OllamaClient(self.base_url) as client:
            return await client.generate(request)
    
    def pull_model(self, model_name: str) -> Dict[str, Any]:
        """Загрузить модель"""
        return asyncio.run(self._async_pull_model(model_name))
    
    async def _async_pull_model(self, model_name: str) -> Dict[str, Any]:
        async with OllamaClient(self.base_url) as client:
            return await client.pull_model(model_name)

# Пример использования
async def example_usage():
    """Пример использования OllamaClient"""
    
    # Асинхронное использование
    async with OllamaClient() as client:
        # Проверка доступности
        if await client.health_check():
            print("✅ Ollama API доступен")
            
            # Список моделей
            models = await client.list_models()
            print(f"📋 Доступные модели: {len(models)}")
            for model in models:
                print(f"  - {model.name} ({model.size} bytes)")
            
            # Генерация ответа
            if models:
                request = OllamaGenerateRequest(
                    model=models[0].name,
                    prompt="Привет! Как дела?",
                    stream=False
                )
                
                response = await client.generate(request)
                print(f"🤖 Ответ: {response.response}")
        else:
            print("❌ Ollama API недоступен")

if __name__ == "__main__":
    # Запуск примера
    asyncio.run(example_usage())
