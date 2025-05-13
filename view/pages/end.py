import streamlit as st
from view.ui.bg import bg  # 배경 유지
from logic.room_manager import load_rooms
from logic.game_flow import get_survival_count
from view.language import get_text

def a6():
    bg()
    st.title(get_text("title_end"))

    st.success(get_text("game_end"))
    st.markdown(f"### {get_text('congrats')}")

    # 방 정보 가져오기
    if "room_code" in st.session_state:
        room_code = st.session_state.room_code
        rooms = load_rooms()

        if room_code in rooms:
            st.markdown("---")
            st.subheader(get_text("results_title"))

            # 총 라운드 수 표시
            total_rounds = rooms[room_code].get("total_rounds", 5)
            st.markdown(get_text("total_rounds", rounds=total_rounds))

            # 플레이어 생존/사망 결과 표시
            max_survived = -1
            winner = ""

            for player_name, player_data in rooms[room_code]["players"].items():
                survived_count = player_data.get("survived_count", 0)
                died_count = total_rounds - survived_count

                survived_text = f"<span style='color: #00cc00;'>{get_text('survived')}: {survived_count}</span>"
                died_text = f"<span style='color: #ff5555;'>{get_text('died')}: {died_count}</span>"

                survived_emoji = "😄 " * survived_count
                died_emoji = "💀 " * died_count

                st.markdown(f"**{player_name}**: {survived_text} | {died_text}", unsafe_allow_html=True)
                st.markdown(f"{survived_emoji}{died_emoji}")

                if survived_count > max_survived:
                    max_survived = survived_count
                    winner = player_name

            # 승자 표시
            if winner:
                st.markdown("---")
                st.markdown(f"### 🏆 {winner}")

    st.markdown("---")
    st.info(get_text("restart_info"))

    if st.button(get_text("restart")):
        current_language = st.session_state.language

        if "room_code" in st.session_state:
            del st.session_state.room_code
        if "player_name" in st.session_state:
            del st.session_state.player_name

        for key in list(st.session_state.keys()):
            if key not in ["language", "page"]:
                del st.session_state[key]

        st.session_state.language = current_language
        st.session_state.page = "start"
        st.rerun()

    st.markdown(get_text("thanks"))
