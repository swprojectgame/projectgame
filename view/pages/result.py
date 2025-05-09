import streamlit as st
import random
import openai
from view.ui.bg import bg2, bg_cl  # type: ignore

# OpenAI 키 설정
openai.api_key = st.secrets["OPENAI_API_KEY"]  # Streamlit secrets에 키 저장 필요

scenario = st.session_state.get("scenario")
strategies = st.session_state.get("input_survive")

def generate_outcome(scenario, strategies):
    """GPT에게 시나리오와 전략을 보내고, 30% 생존 확률 기반으로 허구 섞인 이야기 생성"""
    outcomes = {}

    for player, strat in strategies.items():
        survived = random.random() < 0.3  # 30% 확률로 생존
        outcomes[player] = {
            "strategy": strat,
            "result": "생존" if survived else "사망"
        }

    # GPT 메시지 구성
    strategy_text = "\n".join(
        [f"{name}: {data['strategy']} -> {'생존' if data['result']=='생존' else '사망'}"
         for name, data in outcomes.items()]
    )

    prompt = f"""
시나리오:
{scenario}

각 플레이어는 아래와 같은 생존 전략을 제출했습니다. 이 전략에 대해 약간의 허구와 반전을 섞어 간결한 이야기 형식으로 설명하고, 누가 생존했는지 알려주세요.

전략 목록:
{strategy_text}

결과를 다음과 같은 형식으로 작성해주세요:

[플레이어명] - 이야기 + (생존 or 사망)
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.9
    )

    return response.choices[0].message["content"]

def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")

    st.title("결과")

    # ✅ 세션에 저장된 플레이어 목록과 생존 전략 불러오기
    players = st.session_state.get("players", [])
    survival_strategies = st.session_state.get("input_survive", {})

    if not players or not survival_strategies:
        st.warning("플레이어 목록 또는 생존 전략이 없습니다.")
        return

    # ✅ GPT 결과가 세션에 있는 경우
    if "gpt_result" in st.session_state:
        lines = [line.strip() for line in st.session_state["gpt_result"].split("\n") if line.strip()]

        # ✅ 현재까지 출력된 줄 인덱스 저장
        if "current_line" not in st.session_state:
            st.session_state.current_line = 0

        # ✅ 현재 플레이어
        current_player = players[st.session_state.current_line]

        # ✅ 현재 플레이어의 생존 전략 출력
        st.subheader(f"{current_player}의 생존 전략")
        st.markdown(survival_strategies.get(current_player, "전략이 없습니다."))

        # ✅ GPT 결과 출력
        if st.session_state.current_line < len(players):
            if st.button("다음"):
                gpt_response = generate_outcome(scenario, strategies)
                st.session_state.gpt_result = gpt_response
                st.session_state.current_line += 1
                st.rerun()

        # ✅ 모든 줄이 출력된 경우 → 생존 결과 출력
        else:
            st.subheader("🧍 플레이어 생존 결과")

            # 생존 결과가 세션에 있을 때
            if "survival_result" in st.session_state:
                for player, survived in st.session_state["survival_result"].items():
                    status = "생존 😎" if survived else "사망 💀"
                    st.markdown(f"**{player} {status}**")
            else:
                st.warning("⚠️ 생존 결과 정보가 없습니다.")

             # 👉 다음 라운드로 넘어가는 처리
            if st.button("다음"):
                # 플레이 횟수 증가
                if "play_count" not in st.session_state:
                    st.session_state.play_count = 1
                else:
                    st.session_state.play_count += 1

                # 총 라운드 수 확인
                total_rounds = st.session_state.get("total_rounds", 3)

                if st.session_state.play_count >= total_rounds:
                    # 마지막 라운드라면 최종 결과 페이지로 이동
                    st.session_state.page = "end"
                else:
                    # 다음 라운드 → 랜덤 플레이어에게 시나리오 작성 맡기기
                    players = st.session_state.get("players", [])
                    if players:
                        st.session_state["scenario_writer"] = random.choice(players)
                        st.session_state.page = "scenario"
                    else:
                        st.warning("플레이어 목록이 없습니다.")
                st.rerun()
    else:
        st.warning("GPT 결과가 아직 생성되지 않았습니다.")

    # 로비로 돌아가기 버튼
    if st.button("로비로 돌아가기"):
        st.session_state.page = "lobby"
        st.rerun()
