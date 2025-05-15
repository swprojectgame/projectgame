from logic.room_manager import load_rooms, save_rooms
from api.ai_api import generate_response
import re
import streamlit as st

# ✅ 유저가 행동을 제출
def submit_scenario(code, name, scenario):
    rooms = load_rooms()
    if code in rooms and name in rooms[code]["players"]:
        rooms[code]["players"][name]["scenario"] = scenario
        rooms[code]["players"][name]["submitted"] = True
        save_rooms(rooms)
        return True
    return False

# ✅ 모든 유저가 제출 완료했는지 확인
def check_all_submitted(code):
    rooms = load_rooms()
    if code in rooms:
        return all(p.get("submitted", False) for p in rooms[code]["players"].values())
    return False

# ✅ 결과 생성 (플레이어별 GPT 호출 + 중복 호출 방지)
def generate_result(code):
    rooms = load_rooms()
    if code not in rooms:
        return None
    
    players = rooms[code]["players"]

    # ✅ 문자열(str)일 경우도 대비해 딕셔너리로 강제 초기화
    if not isinstance(rooms[code].get("result"), dict):
        rooms[code]["result"] = {}
    result_data = rooms[code]["result"]

    for name, player in players.items():
        if name in result_data:  # ✅ 이미 생성된 결과가 있으면 건너뜀
            continue

        situation = player.get("situation", "")
        scenario = player.get("scenario", "")
        language = st.session_state.get("language", "ko")

        if language == "en":
            prompt = (
                f"Situation: {situation}\n"
                f"Strategy by {name}: {scenario}\n\n"
                "Describe this strategy as a short fictional story (around 200 characters), with about a 10% chance of survival, and clearly state at the end whether they survived or died."
            )
        else:
            prompt = (
                f"상황: {situation}\n"
                f"플레이어 {name}의 전략: {scenario}\n\n"
                "이 전략에 대해 약간의 허구를 가미한 간결한 이야기 형식으로 설명해줘. "
                "분량은 200자 내외로 제한하고, 생존확률은 10% 정도로 해서, 이야기 마지막 줄에는 반드시 생존인지 사망인지 한 줄로 명확히 판단해서 적어줘."
            )

        try:
            response = generate_response(prompt)
        except Exception as e:
            response = f"[GPT 오류] {e}"

        result_data[name] = response

    rooms[code]["result_order"] = list(players.keys())
    rooms[code]["result_index"] = 0

    update_survival_records(rooms, code, result_data)
    save_rooms(rooms)
    return (
        "\n".join([f"- {name}: {result_data[name]}" for name in result_data]),
        result_data
    )

# ✅ 결과 가져오기 (현재 인덱스 기준)
def get_result(code):
    rooms = load_rooms()
    result_dict = rooms[code].get("result", {})

    if not result_dict or not isinstance(result_dict, dict):
        return None

    result_text = "\n".join([f"- {name}: {text}" for name, text in result_dict.items()])
    return (result_text, result_dict)
            
# ✅ 다음 결과로 넘기기 (방장이 호출)
def next_result(code):
    rooms = load_rooms()
    if code in rooms:
        if "result_index" not in rooms[code]:
            rooms[code]["result_index"] = 0
        rooms[code]["result_index"] += 1
        save_rooms(rooms)

# ✅ 제출 상태 초기화 (라운드 진행 시 사용)
def reset_submissions(code):
    rooms = load_rooms()
    if code in rooms:
        for player in rooms[code]["players"].values():
            player["submitted"] = False
            player["scenario"] = ""
            player["situation"] = ""  # 🔥 초기화 유지
        save_rooms(rooms)

# ✅ 생존 여부 파악 및 누적
def update_survival_records(rooms, code, result_data):
    for name, text in result_data.items():
        normalized = text.replace("\n", " ").replace("\r", " ")
        pattern = re.compile(rf"{re.escape(name)}.*?(생존|survived|Survived)", re.IGNORECASE)
        survived = bool(pattern.search(normalized))

        if "survived_count" not in rooms[code]["players"][name]:
            rooms[code]["players"][name]["survived_count"] = 0

        if survived:
            rooms[code]["players"][name]["survived_count"] += 1

# ✅ 생존 횟수 가져오기
def get_survival_count(code, name):
    rooms = load_rooms()
    if code in rooms and name in rooms[code]["players"]:
        return rooms[code]["players"][name].get("survived_count", 0)
    return 0