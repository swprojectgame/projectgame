import random
from logic.room_manager import load_rooms  # ✅ rooms.json 불러오기용

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
    "눈덮인 산속에 고립되었습니다."
]

# ✅ 무작위로 상황 하나 반환
def get_random_situation():
    return random.choice(SITUATIONS)

# ✅ 게임 종료 여부 판단
def is_game_over(code):
    rooms = load_rooms()
    if code in rooms:
        return rooms[code]["current_round"] > rooms[code]["total_rounds"]
    return True