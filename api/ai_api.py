# 🔁 GPT API 없이 테스트 가능한 더미 버전

import os
import openai

    
from openai import OpenAI

client = OpenAI(api_key="")

def generate_response(prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "당신은 죽음의 게임을 운영하는 AI 심판입니다."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"[GPT 오류] {e}"


## api 호출하는 법
## from api.ai_api import generate_response

## st.write(generate_response("이 상황에서 어떻게 해야 살아남을까?"))
