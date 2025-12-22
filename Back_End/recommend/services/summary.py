# recommend/services/summary.py

from .ai_client import AIClient

def summarize_messages(messages, prev_summary=None):
    """
    messages: ChatMessage queryset/list (role/content 갖고 있음)
    prev_summary: session.summary
    """
    ai = AIClient()

    system = {
        "role": "system",
        "content": (
            "너는 영화 추천 챗봇의 대화를 요약하는 AI다.\n"
            "한국어로 간결하게 요약하라.\n"
            "반드시 포함: (1) 사용자 취향(장르/분위기/제약), (2) 언급된 영화, (3) 미해결 요청.\n"
            "불필요한 수다/중복은 제거."
        )
    }

    user = {
        "role": "user",
        "content": (
            f"[이전 요약]\n{prev_summary or '(없음)'}\n\n"
            "[새 대화]\n" + "\n".join([f"- {m.role}: {m.content}" for m in messages]) +
            "\n\n위 내용을 반영해 업데이트된 요약을 작성해줘."
        )
    }

    return ai.chat([system, user])
