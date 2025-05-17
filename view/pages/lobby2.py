import streamlit as st
import time
from view.transition import fx1
from logic.room_manager import load_rooms, save_rooms

def lobby2():
    if st.session_state.get("page") != "lobby2":
        st.stop()

    # 전체 배경을 검은색으로 설정
    st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: black !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # 검은 배경 + 글자 슬라이드 효과
    fx1()
    time.sleep(4.8)

    # ✅ room_code 세션 존재 여부 확인
    if "room_code" not in st.session_state:
        st.error("room_code 없음. 다시 시작해주세요.")
        st.stop()

    code = st.session_state.room_code
    rooms = load_rooms()

    # ✅ 디버깅 출력
    st.write("[디버깅] 현재 room_code:", code)
    st.write("[디버깅] rooms 내용:", rooms)

    if code not in rooms:
        st.error("room_code에 해당하는 방 정보를 찾을 수 없습니다.")
        st.stop()

    rooms[code]["status"] = "started"
    save_rooms(rooms)

    st.session_state.page = "scenario"
    st.rerun()  # 페이지 전환 강제 실행
