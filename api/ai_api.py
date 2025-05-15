# ✅ 실제 API 호출용 코드 (나중에 활성화하면 됨)

from openai import OpenAI

client = OpenAI(api_key="")

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "당신은 죽음의 게임을 운영하는 AI 심판입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT 오류] {e}"
