import streamlit as st
from view.ui.bg import bg2, bg_cl  # type: ignore
from logic.game_flow import generate_result, get_result, reset_submissions, update_survival_records
from logic.utils import get_random_situation, get_different_situation
from logic.room_manager import assign_random_situation_to_all, load_rooms, save_rooms
from view.language import get_text

# 불필요한 UI 요소 숨기기 함수
def hide_lobby_elements():
    # 특별한 클래스를 가진 모든 컨테이너를 찾아서 제거하는 JS 코드
    hide_js = """
    <script>
    function hideElements() {
        // 라운드 설정 관련 요소 숨기기
        document.querySelectorAll('.stNumberInput').forEach(el => {
            const container = el.closest('.element-container');
            if (container) container.style.display = 'none';
        });
        
        // 특정 버튼만 숨기기 (게임 시작, 게임 방법만 해당)
        document.querySelectorAll('button').forEach(btn => {
            const text = btn.innerText.toLowerCase();
            // 정확한 텍스트 매칭으로 변경 - 다음 라운드, 게임 종료 등의 버튼은 유지
            if ((text.includes('게임') && text.includes('시작')) || 
                text.includes('🚀') || 
                (text.includes('게임') && text.includes('방법'))) {
                const container = btn.closest('.element-container');
                if (container) container.style.display = 'none';
            }
        });
        
        // 텍스트 내용으로 찾기 (라운드 관련 텍스트)
        document.querySelectorAll('p, div, label, span').forEach(el => {
            const text = el.innerText || '';
            // 라운드 설정 관련 텍스트만 숨김 (라운드 표시는 유지)
            if ((text.includes('라운드') && text.includes('진행할')) || 
                (text.includes('라운드') && text.includes('수')) ||
                text.includes('게임 시작')) {
                const container = el.closest('.element-container');
                if (container) container.style.display = 'none';
            }
        });
    }
    
    // 페이지 로드 시 실행
    document.addEventListener('DOMContentLoaded', hideElements);
    
    // 0.5초 간격으로 반복 실행 (동적으로 로드되는 요소 처리)
    setInterval(hideElements, 500);
    </script>
    """
    st.markdown(hide_js, unsafe_allow_html=True)
    
    # 추가 CSS - 중요한 버튼(다음 라운드, 게임 종료)은 유지하도록 수정
    additional_css = """
    <style>
    /* 시작 화면 숨기기 */
    .stApp header {
        display: none !important;
    }
    
    /* 특정 UI 요소만 숨기기 - 선택적인 CSS 선택자 사용 */
    div[data-testid="stExpander"], 
    div.stNumberInput, 
    button:contains("게임 방법"), 
    button:contains("게임 시작"),
    button:contains("방 만들기"),
    button:contains("입장하기"),
    div:has(> p:contains("진행할 라운드")),
    div:has(> p:contains("라운드 수")),
    div:has(> label:contains("라운드 수")),
    div:has(> button:contains("게임 시작")),
    div:has(> button:contains("게임 방법")),
    input[type="number"],
    div:has(input[type="number"]),
    div:has(button:contains("게임 시작")),
    div:has(button:contains("🚀")),
    [data-testid="stVerticalBlock"]:has(div.stNumberInput) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        overflow: hidden !important;
    }
    </style>
    """
    st.markdown(additional_css, unsafe_allow_html=True)

def a5():
    # 페이지 로드 시 불필요한 요소 숨기기
    hide_lobby_elements()
    
    bg_cl()
    bg2("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmE3bTEyMW01bnltaGVyeTR4OXNlcDkxYWpndjhsamN0Nzg2Njk5cyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/kg19fN5BXbZGIDznzG/giphy.gif")
    
    # 영어로 표시되도록 언어 설정
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    st.title(get_text("title_result"))

    code = st.session_state.room_code
    rooms = load_rooms()

    # 🔢 현재 라운드 / 총 라운드 수
    current_round = rooms[code].get("current_round", 1)
    max_round = rooms[code].get("total_rounds", 3)
    
    # 현재 상황 기록
    current_situation = rooms[code].get("situation", "")
    
    # ✅ 결과 불러오기 또는 생성
    result = get_result(code)
    if not result:
        result = generate_result(code)
    
    # ✅ 결과 표시
    st.subheader(get_text("result_heading"))
    st.text_area("", result, height=300)
    
    # 라운드 정보 표시
    st.subheader(f"Round {current_round}/{max_round}")

    # ✅ 마지막 라운드일 경우: 종료 안내 및 버튼 제공
    if current_round >= max_round:
        st.success(get_text("game_end"))
        if st.button(get_text("game_over")):
            # 결과를 다시 한번 업데이트하여 최종 카운트 확인
            if result:
                update_survival_records(code, result)
            
            st.session_state.page = "end"
            st.rerun()
    else:
        # ✅ 다음 라운드로 진행
        if st.button(get_text("next_round")):
            # 결과를 다시 한번 업데이트하여 현재 라운드 카운트 확인
            if result:
                update_survival_records(code, result)
            
            # 현재 라운드 결과가 제대로 저장되었는지 확인
            rooms = load_rooms()  # 최신 데이터 다시 로드
            
            # 라운드 증가
            current_round = rooms[code].get("current_round", 1)
            rooms[code]["current_round"] = current_round + 1
            save_rooms(rooms)
            
            # 제출 상태 초기화 - 이 함수가 라운드별 결과를 올바르게 유지함
            reset_submissions(code)
            
            # 라운드가 증가된 후 새로운 무작위 상황 할당
            rooms = load_rooms()  # 다시 최신 데이터 로드
            updated_round = rooms[code].get("current_round", 1)
            
            # 모든 플레이어에게 동일한, 이전과 다른 새로운 무작위 상황 할당
            for _ in range(3):  # 최대 3번 시도
                success = assign_random_situation_to_all(code)
                if success:
                    # 상황이 실제로 변경되었는지 확인
                    new_rooms = load_rooms()
                    new_situation = new_rooms[code].get("situation", "")
                    if new_situation != current_situation and new_situation:
                        break  # 변경 성공
            
            # 다음 라운드 화면으로 이동
            st.session_state.page = "scenario"
            st.rerun()
            
    # CSS로 시작 화면과 라운드 선택 및 표시 UI 요소 숨기기
    st.markdown("""
    <style>
    /* 시작 화면 숨기기 */
    .stApp header {
        display: none !important;
    }
    
    /* 로비 UI 요소 전체 숨기기 - 더 강력한 선택자 사용 */
    div[data-testid="stExpander"], 
    div.stNumberInput, 
    button:contains("게임 방법"), 
    button:contains("게임 시작"),
    button:contains("방 만들기"),
    button:contains("입장하기"),
    button:contains("방법"),
    button:contains("시작"),
    [data-testid="stHorizontalBlock"] button,
    [data-testid="baseButton-secondary"],
    div:has(> p:contains("진행할 라운드")),
    div:has(> p:contains("라운드 수")),
    div:has(> label:contains("라운드")),
    div:has(> button:contains("게임")),
    div:has(> button:contains("방법")),
    input[type="number"],
    div:has(input[type="number"]),
    div:has(button:contains("게임 시작")),
    div:has(button:contains("🚀")),
    [data-testid="stVerticalBlock"]:has(div.stNumberInput),
    footer {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        position: absolute !important;
        z-index: -9999 !important;
        pointer-events: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        max-height: 0 !important;
        overflow: hidden !important;
    }
    
    /* 특정 컨테이너 요소에 대해 더 강력한 숨김 처리 */
    div:has(> div:has(> button:contains("게임 시작"))),
    div:has(> div:has(> button:contains("게임 방법"))),
    div:has(> p:contains("참가자")),
    div:has(> h3:contains("방 코드")),
    div:has(> div.stSlider),
    div.row-widget.stNumberInput,
    div.element-container:has(div.stNumberInput) {
        display: none !important;
        visibility: hidden !important;
        max-height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* 슬라이드쇼 관련 요소 숨기기 */
    div.element-container:has(div.slide-container),
    div:has(> div:contains("슬라이드")) {
        display: none !important;
    }
    
    /* 추가적인 숨김 처리 - UI 영역 전체 숨김 */
    div.element-container:has(p:contains("진행할 라운드")),
    div.element-container:has(button:contains("게임 시작")),
    div.element-container:has(button:contains("🚀")),
    div.element-container:has(div.stNumberInput) {
        display: none !important;
        height: 0 !important;
        overflow: hidden !important;
        margin: 0 !important;
        padding: 0 !important;
        visibility: hidden !important;
    }
    </style>
    
    <script>
    // 자바스크립트로 추가 제거
    window.addEventListener('DOMContentLoaded', (event) => {
        setTimeout(() => {
            // 게임 시작 버튼 및 라운드 선택 요소 제거
            const removeElements = () => {
                // 텍스트 내용으로 요소 찾기
                document.querySelectorAll('p, button, div, label').forEach(el => {
                    if (el.innerText && (
                        el.innerText.includes('게임 시작') || 
                        el.innerText.includes('라운드 수') ||
                        el.innerText.includes('진행할 라운드') ||
                        el.innerText.includes('🚀')
                    )) {
                        const parent = el.closest('.element-container') || el.parentElement;
                        if (parent) parent.style.display = 'none';
                    }
                });
                
                // 숫자 입력 필드 제거
                document.querySelectorAll('input[type="number"]').forEach(el => {
                    const container = el.closest('.row-widget.stNumberInput');
                    if (container) {
                        const parent = container.closest('.element-container');
                        if (parent) parent.style.display = 'none';
                    }
                });
            };
            
            // 즉시 실행 및 500ms 간격으로 재실행 (동적 로딩 요소 처리)
            removeElements();
            setInterval(removeElements, 500);
        }, 100);
    });
    </script>
    """, unsafe_allow_html=True)
