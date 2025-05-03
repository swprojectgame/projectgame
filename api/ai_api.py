import openai

# 🎯 여기에 OpenAI API 키를 직접 입력 (주의: 깃허브 올릴 땐 꼭 삭제!)
openai.api_key = ""

def generate_response(prompt, model="gpt-4"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "넌 생존 심판관 AI야. 답변을 평가해."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"오류: {e}"


## api 호출하는 법
## from api.ai_api import generate_response

## st.write(generate_response("이 상황에서 어떻게 해야 살아남을까?"))
