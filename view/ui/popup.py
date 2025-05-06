from streamlit_modal import Modal
import streamlit as st
## pip install streamlit-modal 설치 필요!!

# 모달 생성
modal = Modal("방 코드 입력", key="room_modal")
open_modal = st.button("🎮 방 참여하기")

# 모달 열기
if open_modal:
    modal.open()

# 상태 저장용 키
if "room_code" not in st.session_state:
    st.session_state.room_code = ""

# 모달이 열려있을 때
if modal.is_open():
    with modal.container():
        # 코드 입력 필드
        room_code = st.text_input("방 코드를 입력하세요", key="room_code")

        # 입장 버튼 클릭 시 유효성 검사
        if st.button("입장하기"):
            if not room_code.strip():
                st.warning("❗ 코드를 입력해주세요.")
            else:
                st.success(f"✅ '{room_code}' 코드로 입장합니다!")
                # 여기에 작업해주세요!!