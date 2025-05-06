import streamlit as st
from logic.room_manager import create_room, join_room
from view.ui.bg import bg  # type: ignore

# 다국어 텍스트 딕셔너리
TRANSLATIONS = {
    "ko": {
        "title": "🎮 Death by AI - 시작화면",
        "nickname": "닉네임을 입력하세요:",
        "create_room": "🆕 방 만들기",
        "join_room": "🔑 방 코드로 입장",
        "room_created": "✅ 방이 생성되었습니다! 코드: {code}",
        "already_in_room": "이미 '{code}' 방에 입장 중입니다.",
        "enter_nickname_first": "닉네임을 먼저 입력하세요.",
        "enter_room_code": "참여할 방 코드를 입력하세요:",
        "enter": "입장하기",
        "invalid_code": "🚫 유효하지 않은 방 코드입니다."
    },
    "en": {
        "title": "🎮 Death by AI - Start Screen",
        "nickname": "Enter your nickname:",
        "create_room": "🆕 Create Room",
        "join_room": "🔑 Join with Room Code",
        "room_created": "✅ Room created! Code: {code}",
        "already_in_room": "Already in room '{code}'.",
        "enter_nickname_first": "Please enter your nickname first.",
        "enter_room_code": "Enter the room code:",
        "enter": "Enter",
        "invalid_code": "🚫 Invalid room code."
    }
}

def get_text(key, **kwargs):
    """현재 언어 설정에 맞는 텍스트를 반환합니다."""
    if "language" not in st.session_state:
        st.session_state.language = "ko"  # 기본 언어는 한국어
    
    lang = st.session_state.language
    text = TRANSLATIONS[lang].get(key, key)  # 번역이 없으면 키 자체를 반환
    
    # 포맷팅이 필요한 경우 처리
    if kwargs:
        text = text.format(**kwargs)
    
    return text

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
