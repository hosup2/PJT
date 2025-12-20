from .ai_client import AIClient

def summarize_messages(messages, prev_summary=""):
    """
    기존 요약 + 최근 대화를 합쳐 새로운 요약 생성
    """
    ai = AIClient()

    chat_text = "\n".join([
        f"{m.role}: {m.content}"
        for m in messages
    ])

    prompt = f"""
너는 대화 요약 전문가다.
아래는 사용자와 AI의 대화 기록이다.

기존 요약:
{prev_summary}

새 대화:
{chat_text}

위 내용을 바탕으로
✔ 사용자 취향
✔ 선호 장르
✔ 싫어하는 요소
✔ 대화 맥락
을 중심으로 5~6줄 이내로 요약해라.
"""

    return ai.chat(prompt)
