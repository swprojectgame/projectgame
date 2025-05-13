import random
import streamlit as st

# 🎲 Death by AI에서 사용할 위기 상황 리스트
SITUATIONS = [
    "사자가 쫓아오고 있습니다.",
    "좀비가 벽을 뚫고 들어왔습니다.",
    "비행기에서 낙하산 없이 떨어졌습니다.",
    "건물에 불이 났습니다.",
    "우주선 산소가 고갈되고 있습니다.",
    "지진으로 건물이 무너지고 있습니다.",
    "거대한 타임루프에 갇혔습니다.",
    "로봇이 반란을 일으켰습니다.",
    "바다 한가운데서 상어 떼를 만났습니다.",
    "눈덮인 산속에 고립되었습니다.",
    "외계인의 우주선에 납치되었습니다.",
    "독이 든 음식을 먹었습니다.",
    "물 속에 빠져 산소가 부족합니다.",
    "밀폐된 금고에 갇혔습니다.",
    "맹독성 바이러스가 퍼지고 있습니다.",
    "사막 한가운데 물 없이 고립되었습니다.",
    "화산이 폭발하기 시작했습니다.",
    "폭풍우가 치는 바다에서 배가 침몰하고 있습니다.",
    "전쟁 지역에 고립되었습니다.",
    "정글에서 맹수들에게 포위되었습니다."
]

# 영어 상황 리스트 추가
SITUATIONS_EN = [
    "A lion is chasing you.",
    "Zombies have broken through the wall.",
    "You fell from an airplane without a parachute.",
    "The building is on fire.",
    "The spacecraft is running out of oxygen.",
    "The building is collapsing due to an earthquake.",
    "You are trapped in a massive time loop.",
    "Robots have started a rebellion.",
    "You encountered a group of sharks in the middle of the sea.",
    "You are stranded in a snow-covered mountain.",
    "You have been abducted by an alien spaceship.",
    "You ate food containing poison.",
    "You are underwater and running out of oxygen.",
    "You are trapped in a sealed vault.",
    "A deadly virus is spreading.",
    "You are stranded in the middle of a desert without water.",
    "A volcano has started to erupt.",
    "Your ship is sinking in a stormy sea.",
    "You are stranded in a war zone.",
    "You are surrounded by predators in the jungle."
]

# ✅ 무작위로 상황 하나 반환
def get_random_situation():
    if "language" in st.session_state and st.session_state.language == "en":
        return random.choice(SITUATIONS_EN)
    else:
        return random.choice(SITUATIONS)

# ✅ 현재 상황과 다른 새로운 상황을 반환
def get_different_situation(current_situation):
    """현재 상황과 다른 새로운 상황을 반환합니다."""
    if "language" in st.session_state and st.session_state.language == "en":
        # 현재 상황을 제외한 다른 상황 목록 생성
        available_situations = [s for s in SITUATIONS_EN if s != current_situation]
        # 그 중에서 랜덤 선택
        return random.choice(available_situations)
    else:
        # 현재 상황을 제외한 다른 상황 목록 생성
        available_situations = [s for s in SITUATIONS if s != current_situation]
        # 그 중에서 랜덤 선택
        return random.choice(available_situations) 
