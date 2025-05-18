import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.room_manager import load_rooms, save_rooms
from view.language import get_text
from view.ui.cleaner import clean_ui

TIME_LIMIT = 45  # 제한 시간 (초)

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMm9sdWZqdGs5Z3ZudnhsdXRreXd2d3U1bTMxbHAxYmxiOXhnZzhhMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LAsvbjyumSIz67f40e/giphy.gif")
    if st.session_state.get("page") != "prompt":
        st.stop()
    clean_ui(hide_recommend_button=True)

    st.markdown("""
    <script>
    setTimeout(() => {
    const targets = ['추천 시나리오'];
    const allElems = Array.from(document.querySelectorAll('*'));
    for (const el of allElems) {
        const text = el.innerText?.trim();
        if (text && targets.some(t => text === t)) {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        el.style.opacity = '0';
        el.style.height = '0';
        el.style.pointerEvents = 'none';
        }
    }
    }, 500);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <script>
    setTimeout(() => {
    const matches = Array.from(document.querySelectorAll('*'))
        .filter(el =>
        el.innerText &&
        el.innerText.trim() === '추천 시나리오'
        );
    for (const el of matches) {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        el.style.opacity = '0';
        el.style.height = '0';
        el.style.pointerEvents = 'none';
    }
    }, 500);
    </script>
    """, unsafe_allow_html=True)


    st.markdown("""
    <script>
    setTimeout(() => {
    const keywords = ['추천 시나리오'];

    const allElems = Array.from(document.querySelectorAll('*'));
    for (const el of allElems) {
        const text = el.innerText?.trim();
        if (text && keywords.some(t => text === t || text.includes(t))) {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        el.style.opacity = '0';
        el.style.height = '0';
        el.style.pointerEvents = 'none';
        }
    }
    }, 500);
    </script>
    """, unsafe_allow_html=True)

    st.markdown("""
    <script>
    setTimeout(() => {
    const buttons = Array.from(document.querySelectorAll('*'))
        .filter(el => el.innerText && el.innerText.trim() === '추천 시나리오');
        
    for (const el of buttons) {
        el.style.display = 'none';
        el.style.visibility = 'hidden';
        el.style.opacity = '0';
        el.style.height = '0';
        el.style.pointerEvents = 'none';
    }
    }, 500);
    </script>
    """, unsafe_allow_html=True)
    
    if "language" not in st.session_state:
        st.session_state.language = "en"

    st.title(get_text("survival_strategy"))

    if "room_code" not in st.session_state or "player_name" not in st.session_state:
        st.error("세션 정보가 없습니다. 다시 시작해주세요.")
        st.stop()

    code = st.session_state.room_code
    name = st.session_state.player_name
    rooms = load_rooms()


    # ✅ 경과 시간 계산 (모든 유저 공통 기준)
    if "start_time_prompt" not in st.session_state:
        st.session_state["start_time_prompt"] = time.time()

    start_time = st.session_state["start_time_prompt"]

    elapsed = int(time.time() - start_time)
    remaining = max(0, TIME_LIMIT - elapsed)
    host = rooms[code].get("host")

    current_round = rooms[code].get("current_round", 1)
    player_situation = st.session_state.get("player_situation", "상황이 설정되지 않았습니다.")
    st.session_state.player_situation = player_situation  # 백업

    # ✅ 진행 상태 UI
    st.subheader(f"Round {current_round}")
    percent = int((remaining / TIME_LIMIT) * 100)
    blink_class = "blinking-bar" if remaining < 10 else ""
    st.markdown(f"""
        <style>
        @keyframes blink {{
            0% {{ opacity: 1; }}
            100% {{ opacity: 0.4; }}
        }}
        .blinking-bar {{
            animation: blink 1s infinite alternate;
        }}
        </style>
        <div style="background-color:#eee; border-radius:10px; height:20px; width:100%; margin-bottom: 20px;">
            <div class="{blink_class}" style="
                width:{percent}% ;
                background-color:#ff4d4d;
                height:100%;
                border-radius:10px;
                transition: width 1s linear;
            "></div>
        </div>
        <h1 style='text-align: center; font-size: 72px; color: white;'>{remaining}</h1>
    """, unsafe_allow_html=True)

    st.markdown(
        f"<div style='margin-bottom: 12px; font-size: 18px; color: white;'>"
        f"{get_text('current_situation')} {player_situation}"
        f"</div>",
        unsafe_allow_html=True
    )

    # ✅ 전략 입력 및 실시간 세션 저장
    if "input_survive" not in st.session_state:
        st.session_state.input_survive = {}

    strategy_key = f"strategy_{current_round}_{name}"
    strategy = st.text_area(get_text("input_strategy"), height=150, key=strategy_key).strip()
    st.session_state.input_survive[name] = strategy

    # ✅ 본인 전략을 직접 rooms에 저장
    if strategy:
        rooms[code]["players"][name]["strategy"] = strategy
        rooms[code]["players"][name]["submitted"] = True
        save_rooms(rooms)

    st.button(get_text("submit"))  # 유저 위안용 버튼
    if name != host:
        st.markdown(
            "<p style='color: red; font-weight: bold;'>제출 버튼을 클릭해야 작성한 내용이 저장됩니다 !!!</p>",
            unsafe_allow_html=True
        )

    # ✅ 타이머 종료 시 전체 유저 전략 저장
    if remaining == 0:
        rooms = load_rooms()
        for player_name in rooms[code]["players"]:
            strategy = rooms[code]["players"][player_name].get("strategy", "").strip()
            if not strategy:
                rooms[code]["players"][player_name]["strategy"] = get_text("default_strategy")
            rooms[code]["players"][player_name]["submitted"] = True

        save_rooms(rooms)
        st.session_state.page = "result"
        st.rerun()

    # ✅ 타이머 진행 중이면 1초마다 갱신
    if remaining > 0:
        time.sleep(1)
        st.rerun()
