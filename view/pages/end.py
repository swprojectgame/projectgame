import streamlit as st
import time
import json
import os
from view.ui.bg import bg
from logic.room_manager import save_rooms  # load_rooms는 아래에서 교체
from logic.game_flow import get_survival_count,delete_room
from view.language import get_text

# ✅ 안전하게 rooms.json을 읽어오는 함수 (재시도 포함)
def robust_load_rooms(retry=5, delay=0.1):
    for _ in range(retry):
        try:
            if not os.path.exists("rooms.json"):
                return {}
            with open("rooms.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            time.sleep(delay)
    print("❌ rooms.json을 끝내 읽을 수 없습니다.")
    return {}

def a6():
    bg()
    st.title(get_text("title_end"))

    st.success(get_text("game_end"))
    st.markdown(f"### {get_text('congrats')}")

    # 방 정보 가져오기
    if "room_code" in st.session_state:
        room_code = st.session_state.room_code

        rooms = robust_load_rooms()  # ✅ 안전하게 rooms.json 읽기

        if room_code in rooms:
            st.markdown("---")
            st.subheader(get_text("results_title"))

            total_rounds = rooms[room_code].get("total_rounds", 5)
            st.markdown(get_text("total_rounds", rounds=total_rounds))

            max_survived = -1
            winner = ""

            for player_name, player_data in rooms[room_code]["players"].items():
                survived_count = player_data.get("survived_count", 0)
                died_count = player_data.get("died_count", 0)

                survived_text = f"<span style='color: #00cc00;'>{get_text('survived')}: {survived_count}</span>"
                died_text = f"<span style='color: #ff5555;'>{get_text('died')}: {died_count}</span>"

                survived_emoji = "😄 " * survived_count
                died_emoji = "💀 " * died_count

                st.markdown(f"**{player_name}**: {survived_text} | {died_text}", unsafe_allow_html=True)
                st.markdown(f"{survived_emoji}{died_emoji}")

                if survived_count > max_survived:
                    max_survived = survived_count
                    winner = player_name

            if winner:
                st.markdown("---")
                st.markdown(f"### 🏆 {winner}")

            st.markdown("---")
            st.subheader("🏆 플레이어 생존 순위")

            sorted_players = sorted(
                rooms[room_code]["players"].items(),
                key=lambda item: item[1].get("survived_count", 0),
                reverse=True
            )

            for idx, (name, data) in enumerate(sorted_players, start=1):
                count = data.get("survived_count", 0)
                st.markdown(f"**{idx}위** - {name}: {count}회 생존")

    st.markdown("---")
    st.info(get_text("restart_info"))

    if st.button(get_text("restart")):
        current_language = st.session_state.language

        if "room_code" in st.session_state:
            delete_room(st.session_state.room_code)
            del st.session_state.room_code

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