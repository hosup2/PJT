from .ai_client import AIClient

def summarize_messages(messages, prev_summary=None):
    ai = AIClient()

    summary_prompt = f"""
이전 요약:
{prev_summary or "없음"}

아래 대화를 간결하게 요약해라.
중요한 사용자 취향과 맥락을 유지해라.
"""

    chat_messages = [
        {
            "role": "system",
            "content": "너는 대화를 요약하는 AI다."
        },
        {
            "role": "user",
            "content": summary_prompt
        }
    ]

    for msg in messages:
        chat_messages.append({
            "role": msg.role,
            "content": msg.content
        })

    return ai.chat(chat_messages)

