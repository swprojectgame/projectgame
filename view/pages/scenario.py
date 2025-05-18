import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from view.ui.cleaner import clean_ui  # UI 정리 함수 가져오기
from logic.room_manager import load_rooms, save_rooms
from logic.utils import get_random_situation, SITUATIONS
from view.language import get_text
from streamlit_autorefresh import st_autorefresh

TIME_LIMIT = 30  # 제한 시간 (초)
MAX_LENGTH = 140  # 최대 글자 수 제한

def a3():
    st.markdown("""
    <script>
    setTimeout(() => {
    const targets = [
        '게임 방법',
        '방장이 게임 시작을 눌러야 시작됩니다',
        '방장이 게임 시작을 눌러야 시작됩니다. 기다려주세요!',
        '🧠 게임 방법'
    ];
    
    const allElems = Array.from(document.querySelectorAll('*'));
    for (const el of allElems) {
        const text = el.innerText?.trim();
        if (text && targets.some(t => text.includes(t))) {
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
    const targets = ['방장이 게임 시작을 눌러야 시작됩니다', '기다려주세요'];
    const allElems = Array.from(document.querySelectorAll('*'));
    for (const el of allElems) {
        const text = el.innerText?.trim();
        if (text && targets.some(t => text.includes(t))) {
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


    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMm9sdWZqdGs5Z3ZudnhsdXRreXd2d3U1bTMxbHAxYmxiOXhnZzhhMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LAsvbjyumSIz67f40e/giphy.gif")
    if st.session_state.get("page") != "scenario":
        st.stop()
    clean_ui(hide_recommend_button=False)
    
    timer_key = "start_time_scenario"
    
    if timer_key not in st.session_state:
        st.session_state[timer_key] = time.time()

    elapsed = int(time.time() - st.session_state[timer_key])
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

    if "language" not in st.session_state:
        st.session_state.language = "en"

    st.title(get_text("title_scenario"))

    code = st.session_state.room_code
    name = st.session_state.player_name
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)
    host = rooms[code].get("host")

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

    # ✅ 방장만 시나리오 작성 가능
    if name == host:
        st.markdown(f"<div style='text-align: center; font-size: 18px; color: #555;'>{get_text('input_label_scenario')}</div>", unsafe_allow_html=True)

        if "scenario" not in st.session_state:
            st.session_state.scenario = ""

        input_key = f"scenario_input_{current_round}_{name}"
        user_input = st.text_area(
            get_text("notice"),
            key=input_key,
            value=st.session_state.scenario,
            max_chars=MAX_LENGTH,
            height=200
        )

        st.session_state.scenario = user_input

        if st.button(get_text("recommend_button")):
            st.session_state.scenario = get_random_situation()
            st.rerun()

        char_count = len(user_input)
        st.markdown(
            f"<div style='text-align: right; font-size: 14px; color: #888;'>{char_count} / {MAX_LENGTH}자</div>",
            unsafe_allow_html=True
        )
        if st.session_state.get("page") == "scenario":    
            st.markdown(f"<div style='color: red; font-weight: bold;'>{get_text('submit_warning')}</div>", unsafe_allow_html=True)
        st.button(get_text("submit"))  # UI용 버튼

    else:
        st.info("방장이 시나리오를 설정 중입니다...")

    # ✅ 시간 종료 처리
    if remaining == 0:
        if name == host:
            if not st.session_state.scenario.strip():
                st.session_state.scenario = get_random_situation()
            rooms[code]["situation"] = st.session_state.scenario
            save_rooms(rooms)

        # 모든 사용자: 방장이 설정한 시나리오 가져와서 저장
        scenario = rooms[code].get("situation", "")
        rooms[code]["players"][name]["situation"] = scenario
        st.session_state.player_situation = scenario
        save_rooms(rooms)

        st.session_state.page = "prompt"
        st.rerun()

    if remaining > 0:
        time.sleep(1)
        st.rerun()
