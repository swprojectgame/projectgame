import streamlit as st
from logic.room_manager import create_room, join_room
from view.ui.bg import bg  # type: ignore

def a1():
    bg()
    st.title("🎮 Death by AI - 시작화면")

    if "room_code" in st.session_state:
        st.info(f"이미 '{st.session_state.room_code}' 방에 입장 중입니다.")
        return

    # ✅ 방 생성 성공 메시지 출력 (자동 새로고침 방지용)
    if "create_message" in st.session_state:
        st.success(st.session_state.create_message)
        del st.session_state.create_message

    # 🌟 닉네임 입력
    nickname = st.text_input("닉네임을 입력하세요:", key="nickname")

    # 🔀 선택 모드 상태 저장 ("create" or "join")
    if "mode" not in st.session_state:
        st.session_state.mode = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 방 만들기"):
            st.session_state.mode = "create"
    with col2:
        if st.button("🔑 방 코드로 입장"):
            st.session_state.mode = "join"

    st.markdown("---")

    # ✅ 방 만들기 모드
    if st.session_state.mode == "create":
        if nickname:
            room_code = create_room()

            # ✅ 메시지를 세션에 저장해 새로고침 후 유지되도록
            st.session_state.create_message = f"✅ 방이 생성되었습니다! 코드: {room_code}"
            st.session_state.room_code = room_code

            if join_room(room_code, nickname):
                st.session_state.player_name = nickname
                st.session_state.page = "lobby"
                st.rerun()
        else:
            st.warning("닉네임을 먼저 입력하세요.")

    # ✅ 방 참여 모드
    elif st.session_state.mode == "join":
        code_input = st.text_input("참여할 방 코드를 입력하세요:", key="room_code_input")
        if nickname and code_input:
            if st.button("입장하기"):
                if join_room(code_input, nickname):
                    st.session_state.room_code = code_input
                    st.session_state.player_name = nickname
                    st.session_state.page = "lobby"
                    st.rerun()
                else:
                    st.error("🚫 유효하지 않은 방 코드입니다.")
        elif not nickname:
            st.warning("닉네임을 먼저 입력하세요.")