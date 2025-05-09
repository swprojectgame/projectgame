import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import check_all_submitted
from logic.room_manager import load_rooms
from view.language import get_text

TIME_LIMIT = 45  # 제한 시간 (초)
MAX_LENGTH = 140  # 최대 글자 수 제한

def a4():
    bg_cl()
    bg2("https://media3.giphy.com/media/v1.Y2lkPTc5MGI3NjExMTdjNGw4cHE0ZjU2cTFqbGJuM3R6dDBqenlzMTY3aGN3YmpqZ3JrZCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/l87pZAlTSahSABLNqp/giphy.gif")

    # 🔐 필수 정보
    code = st.session_state.room_code
    name = st.session_state.player_name
    
    # 라운드 정보 확인
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)
    
    # 단계 관리
    if "phase" not in st.session_state:
        st.session_state.phase = "input"
    
    # 라운드 변경 감지
    if "last_round" not in st.session_state:
        st.session_state.last_round = 0
        
    # 라운드가 변경되면 phase 초기화
    if current_round != st.session_state.last_round:
        st.session_state.phase = "input"
        st.session_state.last_round = current_round

    # 판단 중인 경우
    if st.session_state.phase == "judging":
        st.markdown("<h1 style='text-align: center; color: white;'>" + get_text("judging") + "</h1>", unsafe_allow_html=True)
        time.sleep(3)
        st.session_state.phase = "finalizing"
        st.rerun()

    # 최종 판단 단계
    elif st.session_state.phase == "finalizing":
        st.markdown("<h1 style='text-align: center; color: white;'>" + get_text("finalizing") + "</h1>", unsafe_allow_html=True)
        time.sleep(3)
        st.session_state.page = "result"
        st.rerun()

    # 입력 단계
    elif st.session_state.phase == "input":
        st.title(get_text("title_prompt"))

        # 모든 플레이어 제출 상태 확인 (문제 방지를 위한 추가 확인)
        submitted = False
        if "players" in rooms[code] and name in rooms[code]["players"]:
            submitted = rooms[code]["players"][name].get("submitted", False)
        
        # 자신이 제출하지 않았는데 다른 화면으로 이동한 경우 수정
        if not submitted and st.session_state.page == "prompt":
            st.info("제출이 완료되지 않았습니다. 시나리오 화면으로 돌아갑니다.")
            time.sleep(2)
            st.session_state.page = "scenario"
            st.rerun()

        # ✅ 모든 플레이어가 제출했는지 확인
        if check_all_submitted(code):
            st.session_state.phase = "judging"
            st.rerun()
        else:
            time.sleep(2)  # 2초 대기 후 새로고침
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
