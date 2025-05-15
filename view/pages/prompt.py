import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.room_manager import load_rooms, save_rooms
from view.language import get_text

TIME_LIMIT = 5  # 제한 시간 (초)

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")

    if "language" not in st.session_state:
        st.session_state.language = "en"

    st.title(get_text("survival_strategy"))

    code = st.session_state.room_code
    name = st.session_state.player_name
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)

    # ✅ 상황은 rooms에서 직접 가져옴
    player_situation = rooms[code]["players"][name].get("situation", "")

    # 타이머 설정
    timer_key = "start_time_prompt"
    if timer_key not in st.session_state:
        st.session_state[timer_key] = time.time()

    elapsed = int(time.time() - st.session_state[timer_key])
    remaining = max(0, TIME_LIMIT - elapsed)

    # 스타일 및 타이머 바 출력
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

    st.subheader(f"Round {current_round}")

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
    st.markdown(f"<h1 style='text-align: center; font-size: 72px; color: white;'>{remaining}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='margin-bottom: 12px; font-size: 18px; color: white;'>{get_text('current_situation')} {player_situation}</div>", unsafe_allow_html=True)

    if "input_survive" not in st.session_state:
        st.session_state.input_survive = {}

    strategy_key = f"strategy_{current_round}_{name}"
    strategy = st.text_area(get_text("input_strategy"), height=150, key=strategy_key)

    st.markdown(f"<div style='color: red; font-weight: bold;'>{get_text('submit_warning')}</div>", unsafe_allow_html=True)
    st.button(get_text("submit"))

    if remaining == 0:
        if not strategy.strip():
            strategy = get_text("default_strategy")

        # ✅ 전략 저장 + 제출 완료 처리
        st.session_state.input_survive[name] = strategy
        rooms[code]["players"][name]["strategy"] = strategy
        rooms[code]["players"][name]["submitted"] = True
        save_rooms(rooms)

        st.session_state.page = "result"
        st.rerun()

    if remaining > 0:
        time.sleep(1)
        st.rerun()
