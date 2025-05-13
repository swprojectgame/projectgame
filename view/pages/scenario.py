import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import submit_scenario
from logic.room_manager import load_rooms
from logic.utils import get_random_situation, SITUATIONS
from view.language import get_text

TIME_LIMIT = 45
MAX_LENGTH = 140

def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")

    code = st.session_state.room_code
    name = st.session_state.player_name

    rooms = load_rooms()

    # 상황이 비어있으면 랜덤으로 배정
    if "players" in rooms[code] and name in rooms[code]["players"] and rooms[code]["players"][name].get("situation", "") == "":
        from logic.room_manager import assign_situation
        if rooms[code].get("situation", "") == "":
            situation = get_random_situation()
            assign_situation(code, situation)
            rooms = load_rooms()

    current_situation = rooms[code]["players"][name].get("situation", "")
    current_round = rooms[code].get("current_round", 1)

    if "last_situation" not in st.session_state:
        st.session_state.last_situation = ""
    if "last_round" not in st.session_state:
        st.session_state.last_round = 0

    if (current_situation != st.session_state.last_situation or 
        current_round != st.session_state.last_round):
        if "user_input" in st.session_state:
            del st.session_state.user_input
        if "start_time" in st.session_state:
            del st.session_state.start_time
        st.session_state.last_situation = current_situation
        st.session_state.last_round = current_round

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TIME_LIMIT - elapsed)

    st.markdown("""
    <style>
    @keyframes blink {
        0% { opacity: 1; }
        100% { opacity: 0.4; }
    }
    .blinking-bar {
        animation: blink 1s infinite alternate;
    }
    </style>
    """, unsafe_allow_html=True)

    st.title(get_text("title_scenario"))

    percent = int((remaining / TIME_LIMIT) * 100)
    blink_class = "blinking-bar" if remaining < 10 else ""
    bar_html = f"""
    <div style="background-color:#eee; border-radius:10px; height:20px; width:100%; margin-bottom: 20px;">
        <div class="{blink_class}" style="
            width:{percent}% ;
            background-color:#ff4d4d;
            height:100%;
            border-radius:10px;
            transition: width 1s linear;
        "></div>
    </div>
    """
    st.markdown(bar_html, unsafe_allow_html=True)

    st.markdown(f"<h1 style='text-align: center; font-size: 72px; color: black;'>{remaining}</h1>", unsafe_allow_html=True)

    if current_situation == "":
        current_situation = get_text("situation_missing")

    st.markdown(get_text("current_situation", situation=current_situation))

    input_key = f"input_{current_round}_{name}"
    user_input = st.text_area(get_text("action_input"), key=input_key, value=st.session_state.user_input, max_chars=MAX_LENGTH)
    st.session_state.user_input = user_input

    char_count = len(user_input)
    st.markdown(f"<div style='text-align: right; font-size: 14px; color: #888;'>{char_count} / {MAX_LENGTH}자</div>", unsafe_allow_html=True)

    if st.button(get_text("submit")):
        if user_input.strip():
            submit_scenario(code, name, user_input.strip())
            st.session_state.page = "prompt"
            st.rerun()

    if remaining == 0 and not user_input.strip():
        st.session_state.page = "result"
        st.rerun()

    st.markdown("""
    <style>
    div.stNumberInput, p:contains("진행할 라운드 수를 선택하세요"),
    div:contains("라운드"), p:contains("라운드") {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    if remaining > 0:
        time.sleep(1)
        st.rerun()
