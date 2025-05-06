from streamlit_modal import Modal
import streamlit as st

modal = Modal("방 코드 입력", key="room_modal")
open_modal = st.button("🎮 방 참여하기")

if open_modal:
    modal.open()

if modal.is_open():
    with modal.container():
        st.text_input("방 코드를 입력하세요")
        st.button("입장하기")
