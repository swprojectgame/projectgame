import streamlit as st
from streamlit_autorefresh import st_autorefresh
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, next_result, reset_submissions
from logic.utils import get_different_situation
from logic.room_manager import assign_situation, load_rooms, save_rooms
from view.language import get_text

def a5():
    code = st.session_state.room_code
    name = st.session_state.player_name
    rooms = load_rooms()
    
    # 🆕 아래 코드 추가 (result_index 아래)
    if name != rooms[code].get("host"):
        current_page = rooms[code].get("page")
        if current_page and current_page != "result":
            st.session_state.page = current_page
            st.rerun()

    # ✅ 방장이 아닐 때만 자동 새로고침 실행
    if name != rooms[code].get("host"):
        st_autorefresh(interval=2000, key="auto_refresh")

    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    st.title(get_text("title_result"))

    if "room_code" not in st.session_state or "player_name" not in st.session_state:
        st.error("세션 정보가 없습니다. 다시 시작해주세요.")
        st.stop()

    # ✅ 결과가 없으면 방장이 생성
    if (
        "result" not in rooms[code]
        or not isinstance(rooms[code]["result"], dict)
        or not all(p in rooms[code]["result"] for p in rooms[code]["players"])
        or "result_index" not in rooms[code]
        or "result_order" not in rooms[code]
    ):
        if name == rooms[code].get("host"):
            generate_result(code)
            rooms = load_rooms()
        else:
            st.info("AI가 판단 중입니다... 방장이 결과를 생성하면 곧 표시됩니다.")
            st.stop()

    # ✅ 현재 결과 출력
    result_index = rooms[code].get("result_index", 0)
    result_order = rooms[code].get("result_order", [])
    result_data = rooms[code].get("result", {})

    if result_index < len(result_order):
        current_name = result_order[result_index]
        current_result = result_data.get(current_name, "결과 없음")

        st.markdown(get_text("result_heading"))
        with st.container():
            st.markdown(f"### 🧑‍💼 {current_name}의 결과", unsafe_allow_html=True)
            st.markdown(
                f"<div style='padding: 1rem; background-color: #f5f5f5; border-radius: 10px; "
                f"border: 1px solid #ccc; color: black; font-size: 16px; line-height: 1.6;'>"
                f"{current_result.replace(chr(10), '<br>')}"
                f"</div>",
                unsafe_allow_html=True
            )

        if name == rooms[code].get("host"):
            if st.button("다음 플레이어 결과 보기"):
                next_result(code)
                st.rerun()
        else:
            st.markdown(
                "<p style='color: gray;'>방장이 결과를 넘기면 자동으로 다음 결과가 표시됩니다.</p>", unsafe_allow_html=True)

    else:
        st.success("모든 플레이어 결과 확인 완료!")

        if name == rooms[code].get("host"):
            if st.button("다음 라운드로 이동"):
                current_round = rooms[code].get("current_round", 1)
                max_round = rooms[code].get("total_rounds", 3)

                if current_round >= max_round:
                    rooms[code]["page"] = "end"
                else:
                    current_situation = rooms[code].get("situation", "")
                    new_situation = get_different_situation(current_situation)
                    assign_situation(code, new_situation)
                    reset_submissions(code)

                    # ✅ 결과 제거 및 다음 라운드 준비
                    rooms[code].pop("result", None)
                    rooms[code].pop("result_order", None)
                    rooms[code].pop("result_index", None)

                    rooms[code]["current_round"] = current_round + 1
                    rooms[code]["page"] = "scenario"

                save_rooms(rooms)
                st.session_state.page = rooms[code]["page"]  # ✅ 세션 상태 업데이트
                st.rerun()

        else:
            page = rooms[code].get("page")
            if page:
                st.session_state.page = page
                st.rerun()
