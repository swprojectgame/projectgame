from logic.room_manager import load_rooms, save_rooms
from api.ai_api import generate_response  # 🔁 GPT API 호출 함수 사용
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

    current_round = rooms[code].get("current_round", 1)  # 🔹 현재 라운드 추출

    # 🔹 GPT에 보낼 프롬프트 구성
    prompt = "당신은 공정하고 창의적인 죽음의 심판관입니다.\n"
    prompt += "다음은 플레이어들이 위기 상황에 대응한 내용입니다.\n\n"

    for name, player in rooms[code]["players"].items():
        situation = player.get("situation", "")
        action = player.get("scenario", "")
        prompt += f"플레이어 '{name}'\n"
        prompt += f"상황: {situation}\n"
        prompt += f"행동: {action}\n"
        prompt += f"결과: "

    prompt += (
        "\n\n각 플레이어의 생존 여부를 유머러스하고 극적으로 판단해 주세요. "
        "결과는 다음과 같이 출력합니다:\n"
        "- 제임스: 사망. 샷건은 가짜였다...\n"
        "- 민지: 생존. 미리 설치해둔 덫이 사자를 잡았다!\n"
    )

    try:
        result_text = generate_response(prompt)
    except Exception as e:
        result_text = f"[GPT 오류] {e}"

    # 🔹 라운드별 결과 저장
    if "results" not in rooms[code]:
        rooms[code]["results"] = {}

    rooms[code]["results"][str(current_round)] = result_text

    update_survival_records(code, result_text)
    save_rooms(rooms)

    return result_text

# ✅ 저장된 결과 불러오기 (현재 라운드 기준)
def get_result(code):
    rooms = load_rooms()
    current_round = rooms[code].get("current_round", 1)
    return rooms[code].get("results", {}).get(str(current_round), "")

# ✅ 다음 라운드를 위해 제출 상태 초기화
def reset_submissions(code):
    rooms = load_rooms()
    if code in rooms:
        for p in rooms[code]["players"].values():
            p["submitted"] = False
            p["scenario"] = ""
        # 🔹 기존 result는 초기화 안 해도 됨 (라운드별 저장으로 변경됨)
        save_rooms(rooms)

# ✅ 결과 텍스트를 파싱하여 생존 여부 판단 및 기록
def update_survival_records(code, result_text):
    rooms = load_rooms()
    if code not in rooms:
        return

    players = list(rooms[code]["players"].keys())

    for player_name in players:
        pattern = r"[-\*]\s*" + re.escape(player_name) + r"\s*[:：]\s*(생존|survived|Survived)"
        alternative_pattern = re.compile(r"[-\*]\s*(.*" + re.escape(player_name) + r".*?)[:：]\s*(생존|survived|Survived)", re.IGNORECASE)

        direct_match = bool(re.search(pattern, result_text, re.IGNORECASE))
        alternative_match = bool(alternative_pattern.search(result_text))
        survived = direct_match or alternative_match

        if "survived_count" not in rooms[code]["players"][player_name]:
            rooms[code]["players"][player_name]["survived_count"] = 0

        if survived:
            rooms[code]["players"][player_name]["survived_count"] += 1

    save_rooms(rooms)

# ✅ 생존 횟수 조회
def get_survival_count(code, player_name):
    rooms = load_rooms()
    if code in rooms and player_name in rooms[code]["players"]:
        return rooms[code]["players"][player_name].get("survived_count", 0)
    return 0
