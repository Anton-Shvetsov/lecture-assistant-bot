import logging
from pathlib import Path
from typing import Optional, Dict, Any
import httpx
from bot.config import settings


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

file_handler = logging.FileHandler("llm_client.log", encoding="utf-8")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


class LLMClient:

    def __init__(self, base_url: Optional[str] = None, timeout: float = 10.0,
                 lectures_dir: Optional[str] = None, model: str = "deepseek-chat"):
        self.base_url = (base_url or settings.deepseek_api_url).rstrip("/")
        self.timeout = timeout
        self.client = httpx.AsyncClient(timeout=self.timeout)
        self.model = model

        if lectures_dir:
            self.lectures_dir = Path(lectures_dir)
        else:
            self.lectures_dir = Path(__file__).parent.parent.parent / "lectures"

        if not self.lectures_dir.exists():
            logger.warning(f"Папка с лекциями {self.lectures_dir} не найдена.")

    def _load_lecture(self, subject: str, lecture: str) -> str:
        """
        Загружает только выбранную лекцию по предмету и названию.
        """
        lecture_file = self.lectures_dir / subject / f"{lecture}.txt"
        if not lecture_file.exists():
            logger.warning(f"Лекция '{lecture}' для предмета '{subject}' не найдена. Используется дефолтный prompt.")
            return ""
        try:
            return lecture_file.read_text(encoding="utf-8")
        except Exception as e:
            logger.error(f"Ошибка при чтении лекции '{lecture}': {e}")
            return ""

    async def chat(
        self,
        user_id: int,
        text: str,
        subject: str,
        lecture: str,
        temperature: float = 1.0,
        max_tokens: int = 2048,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
 
        lecture_text = self._load_lecture(subject, lecture)
        system_prompt = "Ты дружелюбный помощник и профессионал. Отвечай кратко, используя предоставленный материал, на русском."

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": f"{system_prompt}\n\n{lecture_text}"},
                {"role": "user", "content": text}
            ],
            "prefix": True,
            "user_id": user_id,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        if metadata:
            payload["metadata"] = metadata

        try:
            r = await self.client.post(
                f"{self.base_url}/chat/completions",
                json=payload,
                headers={"Authorization": f"Bearer {settings.deepseek_api_key}"}
            )
            r.raise_for_status()
            data = r.json()

            usage = data.get("usage", {})
            cache_hit = usage.get("prompt_cache_hit_tokens")
            cache_miss = usage.get("prompt_cache_miss_tokens")
            completion_tokens = usage.get("completion_tokens")
            total_tokens = usage.get("total_tokens")

            logger.info(
                f"User {user_id} - cache_hit: {cache_hit}, cache_miss: {cache_miss}, "
                f"completion_tokens: {completion_tokens}, total_tokens: {total_tokens}"
            )

            reply = data.get("choices", [{}])[0].get("message", {}).get("content")
            if not reply:
                logger.error(f"Пустой ответ от LLM: {data}")
                return "⚠️ Ошибка: пустой ответ от LLM"

            return reply

        except httpx.RequestError as e:
            logger.error(f"Request failed: {e}")
            return "⚠️ Ошибка соединения с LLM. Попробуй позже."
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error: {e.response.status_code} {e.response.text}")
            return "⚠️ LLM вернул ошибку. Попробуй позже."



llm_client = LLMClient()
