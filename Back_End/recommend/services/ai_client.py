# recommend/services/ai_client.py
import requests
import json
import re
from django.conf import settings


class AIClient:
    def rank_movies(self, prompt: str) -> list[dict]:
        payload = {
            "model": settings.GMS_MODEL,
            "messages": [
                {"role": "system", "content": "너는 영화 추천 전문가 AI다."},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.3,
        }

        response = requests.post(
            settings.GMS_API_URL,
            headers={
                "Authorization": f"Bearer {settings.GMS_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=10,
        )

        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return self._parse_json(content)

    def _parse_json(self, content: str):
        cleaned = re.sub(r"```json|```", "", content).strip()
        return json.loads(cleaned)
