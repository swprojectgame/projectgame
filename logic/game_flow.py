from logic.room_manager import load_rooms, save_rooms
from api.ai_api import generate_response
import streamlit as st
import re

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

# ✅ 결과 생성 (GPT 호출) + 라운드별 결과 저장
def generate_result(code):
    rooms = load_rooms()
    if code not in rooms:
        return None

    # ✅ 이미 결과가 있으면 다시 호출 안 함
    if "result" in rooms[code]:
        return True

    players = rooms[code]["players"]
    prompt = ""
    language = st.session_state.get("language", "ko")

    # 🔹 모든 행동 요약 프롬프트 구성
    for name, p in players.items():
        situation = p.get("situation", "")
        scenario = p.get("scenario", "")
        prompt += f"- {name}: {situation} → {scenario}\n"

    # 🔸 지시문 추가 (언어별)
    if language == "en":
        prompt += (
            "\n\nDescribe this strategy as a concise story with a hint of fiction. "
            "Keep it under 200 characters and clearly state at the end whether the player survived or died."
        )
    else:
        prompt += (
            "\n\n이 전략에 대해 약간의 허구를 가미한 간결한 이야기 형식으로 설명해줘. "
            "분량은 200자 내외로 제한하고, 이야기 마지막 줄에는 반드시 생존인지 사망인지 한 줄로 명확히 판단해서 적어줘."
        )

    try:
        response = generate_response(prompt)
    except Exception as e:
        response = f"[GPT 오류] {e}"

    # ✅ 결과 파싱
    result_data = {}
    for name in players:
        if language == "en":
            pattern = re.compile(rf"{re.escape(name)}.*?(survived|died)", re.IGNORECASE)
        else:
            pattern = re.compile(rf"{re.escape(name)}.*?(생존|사망)", re.IGNORECASE)

        match = pattern.search(response)
        survived = False
        if match:
            status = match.group(1).lower()
            if status in ["생존", "survived"]:
                survived = True
        result_data[name] = {
            "text": response,  # 전체 응답 저장
            "survived": survived
        }

        # 생존 누적 처리
        if "survived_count" not in players[name]:
            players[name]["survived_count"] = 0
        if survived:
            players[name]["survived_count"] += 1

    # ✅ 결과 저장
    rooms[code]["result"] = result_data
    rooms[code]["result_order"] = list(players.keys())
    rooms[code]["result_index"] = 0
    save_rooms(rooms)
    return True


# ✅ 저장된 결과 불러오기
def get_result(code):
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)
    return rooms[code].get("results", {}).get(str(current_round), "")

# ✅ 제출 상태 초기화
def reset_submissions(code):
    rooms = load_rooms()
    if code in rooms:
        for p in rooms[code]["players"].values():
            p["submitted"] = False
            p["scenario"] = ""
        save_rooms(rooms)

# ✅ 결과 텍스트를 파싱하여 생존 여부 판단 및 기록
def update_survival_records(rooms, code, result_text):  # ✅ rooms 인자로 받음
    normalized_text = result_text.replace("\n", " ").replace("\r", " ")
    print(f"📦 생존 판단 시작\n{normalized_text}\n")

    for player_name in rooms[code]["players"]:
        pattern = re.compile(rf"{re.escape(player_name)}.*?(생존|survived|Survived)", re.IGNORECASE)
        survived = bool(pattern.search(normalized_text))
        print(f"🔍 {player_name} → 생존 판정: {survived}")

        if "survived_count" not in rooms[code]["players"][player_name]:
            rooms[code]["players"][player_name]["survived_count"] = 0

        if survived:
            rooms[code]["players"][player_name]["survived_count"] += 1
            print(f"✅ {player_name} survived_count += 1 → {rooms[code]['players'][player_name]['survived_count']}")

    print("💾 저장 준비 완료 (상위에서 save_rooms 실행)")

# ✅ 생존 횟수 조회
def get_survival_count(code, player_name):
    rooms = load_rooms()
    if code in rooms and player_name in rooms[code]["players"]:
        return rooms[code]["players"][player_name].get("survived_count", 0)
    return 0
