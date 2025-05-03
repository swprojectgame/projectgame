import streamlit as st
from logic.room_manager import create_room, get_players, join_room  # ✅ join_room 추가
import socket
from urllib.parse import urlencode

# ✅ URL 파라미터 처리 (자동 입장용)
from logic.url_router import handle_url_params
handle_url_params()


def a0():
    st.title("🧪 서버 기능 테스트 페이지")

    # 1. 이름 입력
    name = st.text_input("당신의 이름을 입력하세요", value=st.session_state.get("player_name", ""))
    if name:
        st.session_state.player_name = name

    # 2. 방 생성
    if "room_code" not in st.session_state:
        if st.button("방 만들기"):
            room_code = create_room()
            st.session_state.room_code = room_code
            # ✅ 방 만든 사람도 참가자 목록에 자동 등록
            join_room(room_code, st.session_state.player_name)
            st.success(f"방이 생성되었습니다! 코드: {room_code}")

    # 3. 초대 링크 만들기
    if "room_code" in st.session_state:
        host_ip = socket.gethostbyname(socket.gethostname())
        room_code = st.session_state.room_code
        params = {"room": room_code, "name": "yourname"}
        query_string = urlencode(params)
        invite_url = f"http://{host_ip}:8501/?{query_string}"

        st.info("👇 친구에게 이 주소를 보내세요!")
        st.code(invite_url, language="url")
        st.button("📋 주소 복사하기", on_click=lambda: st.toast("주소를 복사하세요!"))

        # 4. 현재 참가자 확인
        players = get_players(room_code)
        st.write("현재 참가자:", players)

        # 5. 새로고침
        if st.button("새로고침"):
            st.rerun()
