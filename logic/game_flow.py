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

    current_round = rooms[code].get("current_round", 1)

    # ✅ 중복 호출 방지
    if str(current_round) in rooms[code].get("results", {}):
        return rooms[code]["results"][str(current_round)]

    print(f"🚨 GPT 호출됨 for round {current_round}")

    # 🔹 언어 설정에 따라 프롬프트 구성
    language = st.session_state.get("language", "ko")

    if language == "en":
        prompt = (
            "You are a fair and creative judge in a life-or-death game.\n"
            "Below are how each player responded to their situation:\n\n"
        )
    else:
        prompt = (
            "당신은 공정하고 창의적인 죽음의 심판관입니다.\n"
            "다음은 플레이어들이 위기 상황에 대응한 요약입니다:\n\n"
        )

    # 🔸 상황 요약 입력 (간결하게)
    for name, player in rooms[code]["players"].items():
        situation = player.get("situation", "")
        action = player.get("scenario", "")
        prompt += f"- {name}: {situation} → {action}\n"

    # 🔸 출력 포맷 지시 (GPT에게 명확하게)
    if language == "en":
        prompt += (
            "\n\nPlease determine whether each player survived or died in a humorous and dramatic way.\n"
            "Format the result like this:\n"
            "- James: Died. The shotgun was fake...\n"
            "- Minji: Survived. Her trap caught the lion just in time!\n"
        )
    else:
        prompt += (
            "\n\n각 플레이어의 생존 여부를 유머러스하고 극적으로 판단해 주세요.\n"
            "결과는 다음과 같이 출력합니다:\n"
            "- 제임스: 사망. 샷건은 가짜였다...\n"
            "- 민지: 생존. 미리 설치해둔 덫이 사자를 잡았다!\n"
        )

    try:
        result_text = generate_response(prompt)
    except Exception as e:
        result_text = f"[GPT 오류] {e}"

    # 🔹 결과 저장
    if "results" not in rooms[code]:
        rooms[code]["results"] = {}
    rooms[code]["results"][str(current_round)] = result_text

    update_survival_records(rooms, code, result_text)  # ✅ 수정된 rooms 전달
    save_rooms(rooms)

    return result_text

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
