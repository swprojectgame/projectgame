import streamlit as st
from streamlit_autorefresh import st_autorefresh
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, next_result, reset_submissions
from logic.room_manager import assign_situation, load_rooms, save_rooms  # type: ignore
from view.language import get_text
from logic.utils import get_random_situation

def a5():
    if "room_code" not in st.session_state or "player_name" not in st.session_state:
        st.error("세션 정보가 없습니다. 다시 시작해주세요.")
        st.stop()

    code = st.session_state.room_code
    name = st.session_state.player_name

    rooms = load_rooms()

    if "host" in rooms[code] and name != rooms[code]["host"]:
        current_page = rooms[code].get("page")
        if current_page and current_page != "result":
            st.session_state.page = current_page
            st.rerun()
        st_autorefresh(interval=2000, key="auto_refresh")

    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    st.title(get_text("title_result"))

    if "room_code" not in st.session_state or "player_name" not in st.session_state:
        st.error("세션 정보가 없습니다. 다시 시작해주세요.")
        st.stop()

    # ✅ 결과 없으면 방장이 생성
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
            st.info(get_text("waiting_result"))
            st.stop()

    # ✅ 결과 출력
    result_index = rooms[code].get("result_index", 0)
    result_order = rooms[code].get("result_order", [])
    result_data = rooms[code].get("result", {})

    if result_index < len(result_order):
        current_name = result_order[result_index]
        current_result = result_data.get(current_name, get_text("no_result"))

        # ✅ 전략 가져오기 (빈 문자열도 처리)
        strategy = rooms[code]["players"][current_name].get("strategy", "").strip()

        if not strategy:
            strategy = get_text("default_strategy")
        player_situation = rooms[code]["players"][current_name].get("situation", "상황이 없습니다.")
        
        with st.container():
            st.markdown(f"###  {current_name}의 결과", unsafe_allow_html=True)

            # ✅ 현재 상황 출력
            st.markdown(
                f"<div style='margin-bottom: 12px; font-size: 18px; color: white;'>"
                f"{get_text('current_situation')} {player_situation}"
                f"</div>",
                unsafe_allow_html=True
            )

            # ✅ 전략 출력
            st.markdown(
                f"""
                <div style='margin-bottom: 16px; font-size: 18px; color: #00ffff; font-weight: 500;'>
                    <strong>{get_text("submitted_strategy")}:</strong> {strategy}
                </div>
                """,
                unsafe_allow_html=True
            )

            # ✅ 결과 출력
            st.markdown(
                f"<div style='padding: 1rem; background-color: #f5f5f5; border-radius: 10px; "
                f"border: 1px solid #ccc; color: black; font-size: 16px; line-height: 1.6;'>"
                f"{current_result.replace(chr(10), '<br>')}"
                f"</div>",
                unsafe_allow_html=True
            )

            # ✅ 다음 결과로 넘기기
            if name == rooms[code].get("host"):
                if st.button(get_text("next_result_button")):
                    next_result(code)
                    st.rerun()
            else:
                st.markdown(
                    "<p style='color: gray;'>방장이 결과를 넘기면 자동으로 다음 결과가 표시됩니다.</p>",
                    unsafe_allow_html=True
                )

    else:
        st.success(get_text("game_end"))

        # ✅ 모든 플레이어 전략 출력
        players = rooms[code]["players"]
        st.markdown("### 제출된 생존 전략 요약")
        for player_name, player_data in players.items():
            strategy = player_data.get("strategy", "").strip()
            if not strategy:
                strategy = "전략이 제출되지 않았습니다."

            st.markdown(
                f"<div style='margin-bottom: 8px; font-size: 16px; color: white;'>"
                f"<strong>{player_name}</strong>: {strategy}"
                f"</div>",
                unsafe_allow_html=True
            )

        # ✅ 다음 라운드 or 종료
        if name == rooms[code].get("host"):
            if st.button(get_text("game_over") if rooms[code].get("current_round", 1) >= rooms[code].get("total_rounds", 3) else get_text("next_round")):
                current_round = rooms[code].get("current_round", 1)
                max_round = rooms[code].get("total_rounds", 3)

                if current_round >= max_round:
                    rooms[code]["page"] = "end"
                else:
                    new_situation = get_random_situation()
                    assign_situation(code, new_situation)
                    reset_submissions(code)

                    # ✅ 결과 제거 및 다음 라운드 준비
                    rooms[code].pop("result", None)
                    rooms[code].pop("result_order", None)
                    rooms[code].pop("result_index", None)

                    rooms[code]["current_round"] = current_round + 1
                    rooms[code]["page"] = "scenario"

                save_rooms(rooms)
                st.session_state.page = rooms[code]["page"]
                st.rerun()
        else:
            st.info(get_text("moving_next_round"))
