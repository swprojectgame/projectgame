import streamlit as st
import time
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import submit_scenario
from logic.room_manager import load_rooms
from logic.utils import get_random_situation, SITUATIONS
from view.language import get_text

TIME_LIMIT = 45
MAX_LENGTH = 140

def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")

    code = st.session_state.room_code
    name = st.session_state.player_name

    rooms = load_rooms()

    if "players" in rooms[code] and name in rooms[code]["players"] and rooms[code]["players"][name].get("situation", "") == "":
        from logic.room_manager import assign_situation
        if rooms[code].get("situation", "") == "":
            situation = get_random_situation()
            assign_situation(code, situation)
            rooms = load_rooms()

    current_situation = rooms[code]["players"][name].get("situation", "")
    current_round = rooms[code].get("current_round", 1)

    if "last_situation" not in st.session_state:
        st.session_state.last_situation = ""
    if "last_round" not in st.session_state:
        st.session_state.last_round = 0

    if (current_situation != st.session_state.last_situation or 
        current_round != st.session_state.last_round):
        if "user_input" in st.session_state:
            del st.session_state.user_input
        if "start_time" in st.session_state:
            del st.session_state.start_time
        st.session_state.last_situation = current_situation
        st.session_state.last_round = current_round

    if "start_time" not in st.session_state:
        st.session_state.start_time = time.time()
    if "user_input" not in st.session_state:
        st.session_state.user_input = ""

    elapsed = int(time.time() - st.session_state.start_time)
    remaining = max(0, TIME_LIMIT - elapsed)

    st.title(get_text("title_scenario"))

    st.markdown(get_text("current_situation", situation=current_situation))

    input_key = f"input_{current_round}_{name}"
    user_input = st.text_area(get_text("action_input"), key=input_key, value=st.session_state.user_input, max_chars=MAX_LENGTH)
    st.session_state.user_input = user_input

    if st.button(get_text("submit")):
        if user_input.strip():
            success = submit_scenario(code, name, user_input.strip())
            if success:
                st.session_state.page = "prompt"
                st.rerun()
            else:
                st.warning("제출 실패. 다시 시도해주세요.")

    if remaining == 0 and not user_input.strip():
        st.session_state.page = "result"
        st.rerun()

    if remaining > 0:
        time.sleep(1)
        st.rerun()
