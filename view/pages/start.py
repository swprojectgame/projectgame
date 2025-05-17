import streamlit as st
from logic.room_manager import create_room, join_room
from view.ui.bg import bg  # type: ignore
from view.language import get_text
from streamlit_modal import Modal  # pip install 필요

def a1():
    bg()
    st.title(get_text("title"))

    if "room_code" in st.session_state:
        st.info(get_text("already_in_room", code=st.session_state.room_code))
        return

    if "create_message" in st.session_state:
        st.success(st.session_state.create_message)
        del st.session_state.create_message

    nickname = st.text_input(get_text("nickname"), key="nickname")

    if "mode" not in st.session_state:
        st.session_state.mode = None

    col1, col2 = st.columns(2)
    with col1:
        if st.button(get_text("create_room")):
            st.session_state.mode = "create"
    with col2:
        open_modal = st.button(get_text("join_room"))  # join 버튼 → 모달 열기 트리거

    # 모달 설정
    modal = Modal(get_text("enter_room_code"), key="room_modal")
    if open_modal:
        modal.open()

    if modal.is_open():
        with modal.container():
            code_input = st.text_input(get_text("enter_room_code"), key="room_code_input_modal", max_chars=4)

            if st.button(get_text("enter")):
                if not nickname:
                    st.warning(get_text("enter_nickname_first"))
                elif not code_input.strip():
                    st.warning(get_text("enter_code_first"))
                else:
                    if join_room(code_input, nickname):
                        st.session_state.room_code = code_input
                        st.session_state.player_name = nickname
                        st.session_state.page = "lobby"
                        st.rerun()
                    else:
                        st.error(get_text("invalid_code"))

    st.markdown("---")

    if st.session_state.mode == "create":
        if nickname:
            room_code = create_room(nickname)
            st.session_state.create_message = get_text("room_created", code=room_code)
            st.session_state.room_code = room_code

            if join_room(room_code, nickname):
                st.session_state.player_name = nickname
                st.session_state.page = "lobby"
                st.rerun()
        else:
            st.warning(get_text("enter_nickname_first"))