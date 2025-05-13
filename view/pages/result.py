import streamlit as st
import random
from openai import OpenAI
from view.ui.bg import bg2, bg_cl  # type: ignore
from view.language import get_text  # 다국어 함수 import

client = OpenAI(api_key="sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")

scenario = st.session_state.get("scenario")
strategies = st.session_state.get("input_survive")

def generate_outcome(scenario, strategies):
    outcomes = {}

    for player, strat in strategies.items():
        survived = random.random() < 0.3
        outcomes[player] = {
            "strategy": strat,
            "result": get_text("survived") if survived else get_text("died")
        }

    st.session_state["survival_result"] = {
        player: (data["result"] == get_text("survived")) for player, data in outcomes.items()
    }

    strategy_text = "\n".join(
        [f"{name}: {data['strategy']} -> {data['result']}"
         for name, data in outcomes.items()]
    )

    prompt = f"""
시나리오:
{scenario}

각 플레이어는 아래와 같은 생존 전략을 제출했습니다. 이 전략에 대해 약간의 허구와 반전을 섞어 간결한 이야기 형식으로 설명하고, 누가 생존했는지 알려주세요.

전략 목록:
{strategy_text}

결과를 다음과 같은 형식으로 작성해주세요:

[플레이어명] - 이야기 + ({get_text("survived")} or {get_text("died")})
    """

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{
            "role": "user",
            "content": prompt
        }],
        temperature=0.9
    )

    return response.choices[0].message.content.strip()


def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")

    st.title(get_text("title_result"))

    players = st.session_state.get("players", [])
    survival_strategies = st.session_state.get("input_survive", {})

    if not players or not survival_strategies:
        st.warning(get_text("warning_empty"))
        return

    if "gpt_result" not in st.session_state:
        gpt_response = generate_outcome(scenario, strategies)
        st.session_state["gpt_result"] = gpt_response
        st.session_state["current_line"] = 0

    lines = [line.strip() for line in st.session_state["gpt_result"].split("\n") if line.strip()]
    current_index = st.session_state.get("current_line", 0)

    if current_index < len(players):
        current_player = players[current_index]
        st.subheader(f"{current_player} {get_text('action_input')}")
        st.markdown(survival_strategies.get(current_player, get_text("warning_empty")))

        if current_index < len(lines):
            st.text(lines[current_index])

        if st.button(get_text("next")):
            st.session_state["current_line"] += 1
            st.rerun()
    else:
        st.subheader(get_text("results_title"))
        survival_result = st.session_state.get("survival_result", {})

        for player, survived in survival_result.items():
            status = f"{get_text('survived')} 😎" if survived else f"{get_text('died')} 💀"
            st.markdown(f"**{player} {status}**")

        if st.button(get_text("next_round")):
            st.session_state["play_count"] = st.session_state.get("play_count", 1) + 1
            total_rounds = st.session_state.get("total_rounds", 3)

            if st.session_state["play_count"] >= total_rounds:
                st.session_state.page = "end"
            else:
                st.session_state["scenario_writer"] = random.choice(players)
                st.session_state.page = "scenario"
            st.rerun()

    if st.button(get_text("back_to_lobby")):
        st.session_state.page = "lobby"
        st.rerun()
