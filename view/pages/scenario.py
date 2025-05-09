import streamlit as st
import json
import os
import random
from view.ui.bg import bg2, bg_cl  # type: ignore

STORY_FILE = "story.json"  # 시나리오들이 담긴 JSON 파일 경로

def load_random_scenario():
    if not os.path.exists(STORY_FILE):
        return "⚠️ 시나리오 파일이 존재하지 않습니다."
    with open(STORY_FILE, "r", encoding="utf-8") as f:
        story_list = json.load(f)
    if not isinstance(story_list, list) or not story_list:
        return "⚠️ 시나리오 리스트가 비어 있습니다."
    return random.choice(story_list)

def a3():
    bg_cl()
    bg2("https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNmpqMmZjbXhhNjNqY2NnZjh0OTI2bGVtNzFldGh6c3Fkamh0emVkMiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/PNQi3nT7CVE3JFiRot/giphy.gif")
    
    st.title("어떤 상황을 연출하시겠습니까?")

    # 시나리오 초기화
    if "scenario" not in st.session_state:
        st.session_state.scenario = ""

    # 시나리오 입력 창
    st.session_state.scenario = st.text_area("시나리오를 작성해주세요", value=st.session_state.scenario, height=200)

    # 추천 시나리오 버튼
    if st.button("추천 시나리오"):
        st.session_state.scenario = load_random_scenario()
        st.rerun()

    # 제출 버튼
    if st.button("제출"):
        if st.session_state.scenario.strip():
            st.session_state.page = "prompf"
            st.rerun()
        else:
            st.warning("시나리오를 입력하거나 추천 시나리오를 선택해주세요.")
