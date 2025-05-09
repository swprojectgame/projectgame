import streamlit as st
from logic.room_manager import create_room, join_room
from view.ui.bg import bg  # type: ignore
from view.language import get_text

def a1():
    bg()
    st.title(get_text("title"))

    if "room_code" in st.session_state:
        st.info(get_text("already_in_room", code=st.session_state.room_code))
        return

    # ✅ 방 생성 성공 메시지 출력 (자동 새로고침 방지용)
    if "create_message" in st.session_state:
        st.success(st.session_state.create_message)
        del st.session_state.create_message

    # 🌟 닉네임 입력
    nickname = st.text_input(get_text("nickname"), key="nickname")

    # 🔀 선택 모드 상태 저장 ("create" or "join")
    if "mode" not in st.session_state:
        st.session_state.mode = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("create_room")):
            st.session_state.mode = "create"
    with col2:
        if st.button(get_text("join_room")):
            st.session_state.mode = "join"

    st.markdown("---")

    # ✅ 방 만들기 모드
    if st.session_state.mode == "create":
        if nickname:
            room_code = create_room()

            # ✅ 메시지를 세션에 저장해 새로고침 후 유지되도록
            st.session_state.create_message = get_text("room_created", code=room_code)
            st.session_state.room_code = room_code

            if join_room(room_code, nickname):
                st.session_state.player_name = nickname
                st.session_state.page = "lobby"
                st.rerun()
        else:
            st.warning(get_text("enter_nickname_first"))

    # ✅ 방 참여 모드
    elif st.session_state.mode == "join":
        code_input = st.text_input(get_text("enter_room_code"), key="room_code_input")
        if nickname and code_input:
            if st.button(get_text("enter")):
                if join_room(code_input, nickname):
                    st.session_state.room_code = code_input
                    st.session_state.player_name = nickname
                    st.session_state.page = "lobby"
                    st.rerun()
                else:
                    st.error(get_text("invalid_code"))
        elif not nickname:
            st.warning(get_text("enter_nickname_first"))
