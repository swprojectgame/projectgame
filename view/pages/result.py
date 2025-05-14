import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, reset_submissions
from logic.utils import get_different_situation
from logic.room_manager import assign_situation, load_rooms, save_rooms
from view.language import get_text
from streamlit_autorefresh import st_autorefresh

def a5():
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    st.title(get_text("title_result"))

    code = st.session_state.room_code
    name = st.session_state.player_name
    rooms = load_rooms()

    result_data = rooms[code].get("result", {})
    order = rooms[code].get("result_order", [])
    index = rooms[code].get("result_index", 0)
    current_round = rooms[code].get("current_round", 1)
    total_rounds = rooms[code].get("total_rounds", 3)

    # ✅ GPT 결과 없으면 방장이 생성
    if not result_data:
        if name == rooms[code].get("host"):
            generate_result(code)
            rooms = load_rooms()
        else:
            st.info("AI가 결과를 생성하고 있어요. 잠시만 기다려주세요.")
            st_autorefresh(interval=2000, key="waiting_result")
            return

    # ✅ 플레이어별 결과 출력
    if index < len(order):
        current_player = order[index]
        result_entry = result_data.get(current_player, {})
        st.markdown(f"**{current_player}**의 결과:")
        st.text_area("AI 응답", result_entry.get("text", "결과 없음"), height=200, label_visibility="collapsed")

        # ✅ 방장만 "다음 결과 보기" 가능
        if name == rooms[code].get("host"):
            if st.button(get_text("next_result"), key="next_result_btn"):
                if index < len(order) - 1:
                    rooms[code]["result_index"] += 1
                    save_rooms(rooms)
                    st.rerun()  # ✅ 중간에만 rerun
            else:
                st.info("이미 마지막 결과입니다.")

        else:
            st_autorefresh(interval=2000, key="watching_result")

    # ✅ 모든 결과 출력 완료
    else:
        st.success("모든 플레이어의 결과를 확인했습니다.")

        if name == rooms[code].get("host"):
            if current_round >= total_rounds:
                if st.button(get_text("game_over")):
                    st.session_state.page = "end"
                    st.rerun()
            else:
                if st.button(get_text("next_round")):
                    new_situation = get_different_situation(rooms[code].get("situation", ""))
                    assign_situation(code, new_situation)
                    reset_submissions(code)
                    rooms[code]["current_round"] += 1
                    rooms[code]["result_index"] = 0  # 인덱스 초기화
                    save_rooms(rooms)
                    st.session_state.page = "scenario"
                    st.rerun()
        else:
            st_autorefresh(interval=2000, key="wait_next_round")
