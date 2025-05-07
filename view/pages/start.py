import streamlit as st
from logic.room_manager import create_room, join_room
from view.ui.bg import bg  # type: ignore
from streamlit_modal import Modal  # 무조건 pip install streamlit-modal 따로 설치 필요해용

def a1():
    bg()
    st.title("🎮 Death by AI - 시작화면")

    if "room_code" in st.session_state:
        st.info(f"이미 '{st.session_state.room_code}' 방에 입장 중입니다.")
        return

    if "create_message" in st.session_state:
        st.success(st.session_state.create_message)
        del st.session_state.create_message

    nickname = st.text_input("닉네임을 입력하세요:", key="nickname")

    if "mode" not in st.session_state:
        st.session_state.mode = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button("🆕 방 만들기"):
            st.session_state.mode = "create"
    with col2:
        open_modal = st.button("🔑 방 코드로 입장")  # 모달 트리거

    modal = Modal("방 코드 입력", key="room_modal") # 모달 생성함
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            code_input = st.text_input("방 코드를 입력하세요", key="room_code_input_modal")
            if st.button("입장하기"):
                if not nickname:
                    st.warning("닉네임을 먼저 입력하세요.")
                elif not code_input.strip():
                    st.warning("❗ 코드를 입력해주세요.")
                else:
                    if join_room(code_input, nickname):
                        st.session_state.room_code = code_input
                        st.session_state.player_name = nickname
                        st.session_state.page = "lobby"
                        st.rerun()
                    else:
                        st.error("🚫 유효하지 않은 방 코드입니다.")

    st.markdown("---")

    if st.session_state.mode == "create":
        if nickname:
            room_code = create_room()
            st.session_state.create_message = f"✅ 방이 생성되었습니다! 코드: {room_code}"
            st.session_state.room_code = room_code

            if join_room(room_code, nickname):
                st.session_state.player_name = nickname
                st.session_state.page = "lobby"
                st.rerun()
        else:
            st.warning("닉네임을 먼저 입력하세요.")
