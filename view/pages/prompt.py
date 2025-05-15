import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.room_manager import load_rooms, save_rooms
from view.language import get_text
from view.ui.cleaner import clean_ui  # 추가: UI 정리 함수 가져오기

TIME_LIMIT = 10  # 제한 시간 (초)

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")

    # UI 정리: 게임시작화면 요소 숨기기 (추천 버튼도 숨김)
    clean_ui(hide_recommend_button=True)

    # 언어 기본값 설정
    if "language" not in st.session_state:
        st.session_state.language = "en"

    st.title(get_text("survival_strategy"))

    # 필수 정보 로드
    code = st.session_state.room_code
    name = st.session_state.player_name
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)

    # 플레이어 상황 로드
    player_situation = st.session_state["player_situation"]

    # 타이머 키 초기화
    timer_key = "start_time_prompt"
    if timer_key not in st.session_state:
        st.session_state[timer_key] = time.time()

    # 타이머 계산
    elapsed = int(time.time() - st.session_state[timer_key])
    remaining = max(0, TIME_LIMIT - elapsed)

    # 깜빡임 스타일 추가
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

    # 라운드 표시
    st.subheader(f"Round {current_round}")

    # 타이머 바
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

    # 남은 시간 표시
    st.markdown(f"<h1 style='text-align: center; font-size: 72px; color: white;'>{remaining}</h1>", unsafe_allow_html=True)

    # 상황 표시 (다국어)
    st.markdown(f"<div style='margin-bottom: 12px; font-size: 18px; color: white;'>{get_text("current_situation")} {player_situation}</div>", unsafe_allow_html=True)

    # 전략 입력 필드
    if "input_survive" not in st.session_state:
        st.session_state.input_survive = {}

    strategy_key = f"strategy_{current_round}_{name}"
    strategy = st.text_area(get_text("input_strategy"), height=150, key=strategy_key)

    # st.markdown(f"<div style='color: red; font-weight: bold;'>{get_text('submit_warning')}</div>", unsafe_allow_html=True)
    
    st.button(get_text("submit"))

    if remaining == 0:
        # 입력 없으면 기본 전략
        if not strategy.strip():
            strategy = get_text("default_strategy")

        # ✅ 세션에 저장
        st.session_state.input_survive[name] = strategy

        # ✅ rooms 데이터에 전략 저장
        rooms[code]["players"][name]["strategy"] = strategy
        save_rooms(rooms)  # 변경사항 저장

        st.session_state.page = "result"
        st.rerun()

    if remaining > 0:
        time.sleep(1)
        st.rerun()
