import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import submit_scenario
from logic.room_manager import load_rooms
from logic.utils import get_random_situation, SITUATIONS
from view.language import get_text

TIME_LIMIT = 45  # 제한 시간 (초)
MAX_LENGTH = 140  # 최대 글자 수 제한

def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")

    # 🔐 필수 세션 정보
    code = st.session_state.room_code
    name = st.session_state.player_name
    
    # 현재 상황 및 라운드 정보 로드
    rooms = load_rooms()
    
    # 첫 게임 시작 시 상황이 비어있는 경우 상황 할당 확인
    if "players" in rooms[code] and name in rooms[code]["players"] and rooms[code]["players"][name].get("situation", "") == "":
        from logic.room_manager import assign_situation
        # 방 전체의 상황 확인
        if rooms[code].get("situation", "") == "":
            # 상황이 지정되지 않은 경우 랜덤 상황 할당
            situation = get_random_situation()
            assign_situation(code, situation)
            # 최신 정보로 rooms 갱신
            rooms = load_rooms()
    
    current_situation = ""
    if "players" in rooms[code] and name in rooms[code]["players"]:
        current_situation = rooms[code]["players"][name].get("situation", "")
    current_round = rooms[code].get("current_round", 1)
    
    # 새 라운드 감지 및 입력값 초기화 로직
    if "last_situation" not in st.session_state:
        st.session_state.last_situation = ""
    
    if "last_round" not in st.session_state:
        st.session_state.last_round = 0
    
    # 상황이 변경되거나 라운드가 변경되면 입력값 초기화
    if (current_situation != st.session_state.last_situation or 
        current_round != st.session_state.last_round):
        # 입력값 완전 초기화
        if "user_input" in st.session_state:
            del st.session_state.user_input
        if "start_time" in st.session_state:
            del st.session_state.start_time
        
        # 현재 상황과 라운드 기록
        st.session_state.last_situation = current_situation
        st.session_state.last_round = current_round
    
    # 상태 초기화
    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    # 시간 계산
    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TIME_LIMIT - elapsed)

    # 깜빡임 스타일 정의
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

    # 타이머 바 표시
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
    
    # 타이머 숫자 표시
    st.markdown(f"<h1 style='text-align: center; font-size: 72px; color: black;'>{remaining}</h1>", unsafe_allow_html=True)

    # ✅ 현재 플레이어의 상황 불러오기
    situation = ""
    if "players" in rooms[code] and name in rooms[code]["players"]:
        situation = rooms[code]["players"][name].get("situation", "")
    
    # 상황이 여전히 비어있는 경우 기본 상황 표시
    if situation == "":
        situation = "상황 정보가 로드되지 않았습니다. 새로고침을 시도해보세요."
        
    st.markdown(get_text("current_situation", situation=situation))

    # ✅ 사용자 행동 입력 - key를 고유하게 만들어 캐시 이슈 방지
    input_key = f"input_{current_round}_{name}"
    user_input = st.text_area(get_text("action_input"), key=input_key, value=st.session_state.user_input, max_chars=MAX_LENGTH)
    st.session_state.user_input = user_input  # 입력값 업데이트
    
    char_count = len(user_input)
    st.markdown(
        f"<div style='text-align: right; font-size: 14px; color: #888;'>{char_count} / {MAX_LENGTH}자</div>",
        unsafe_allow_html=True
    )

    # ✅ 제출 버튼 클릭 시 행동 저장 및 다음 페이지 이동
    if st.button(get_text("submit")):
        if user_input.strip():
            submit_scenario(code, name, user_input.strip())
            st.session_state.page = "prompt"  # 대기 화면으로 전환
            st.rerun()

    # 시간 종료 처리
    if remaining == 0 and not user_input.strip():
        st.session_state.page = "result"
        st.rerun()

    # CSS로 라운드 관련 UI 요소 숨기기
    st.markdown("""
    <style>
    /* 라운드 선택 및 관련 UI 요소 숨기기 */
    div.stNumberInput, p:contains("진행할 라운드 수를 선택하세요"),
    div:contains("라운드"), p:contains("라운드") {
        display: none !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 1초마다 화면 갱신
    if remaining > 0:
        time.sleep(1)
        st.rerun()
