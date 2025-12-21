import requests
import json
import re
from django.conf import settings


class AIClient:
    def _request(self, messages):
        response = requests.post(
            settings.GMS_API_URL,
            headers={
                "Authorization": f"Bearer {settings.GMS_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": settings.GMS_MODEL,
                "messages": messages,
                "temperature": 0.3,
            },
            timeout=15,
        )

        response.raise_for_status()
        return response.json()

    def _parse_json(self, content: str):
        """
        ```json ... ``` 제거 + json.loads
        """
        try:
            cleaned = re.sub(r"```json|```", "", content).strip()
            return json.loads(cleaned)
        except Exception:
            return None

    def chat(self, messages: list[dict]) -> str:
        res = self._request(messages)
        return res["choices"][0]["message"]["content"]


    def rank_movies(self, prompt: str):
        res = self._request([
            {"role": "system", "content": "너는 영화 추천 전문가다."},
            {"role": "user", "content": prompt},
        ])

        content = res["choices"][0]["message"]["content"]

        parsed = self._parse_json(content)

        # ✅ 파싱 실패 시 빈 리스트 반환 (절대 서버 터지지 않게)
        if not isinstance(parsed, list):
            return []

        return parsed
