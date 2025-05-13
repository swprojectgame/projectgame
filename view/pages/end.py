#result.py 이후로 나오는 게임 종료 화면
import streamlit as st
from view.ui.bg import bg  # 배경 유지
from logic.room_manager import load_rooms
from logic.game_flow import get_survival_count
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
            // 정확한 텍스트 매칭으로 변경 - 재시작 등의 버튼은 유지
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
            // 라운드 설정 관련 텍스트만 숨김
            if ((text.includes('라운드 수') || text.includes('진행할 라운드')) &&
                !text.includes('결과')) { // '결과' 포함 요소는 유지
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
    
    # 추가 CSS - 중요한 버튼(재시작 버튼)은 유지하도록 수정
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

def a6():
    # 페이지 로드 시 불필요한 요소 숨기기
    hide_lobby_elements()
    
    bg()
    
    # 영어로 표시되도록 언어 설정
    if "language" not in st.session_state:
        st.session_state.language = "en"
    
    st.title(get_text("title_end"))

    st.success(get_text("game_end"))
    st.markdown(f"### {get_text('congrats')}")

    # 방 정보 가져오기
    if "room_code" in st.session_state:
        room_code = st.session_state.room_code
        rooms = load_rooms()
        
        if room_code in rooms:
            # 결과 표시 구역
            st.markdown("---")
            st.subheader(get_text("results_title"))
            
            # 총 라운드 수 표시
            total_rounds = rooms[room_code].get("total_rounds", 5)
            st.markdown(get_text("total_rounds", rounds=total_rounds))
            
            # 플레이어 데이터 수집 및 생존 횟수 기준으로 정렬
            players_data = []
            for player_name, player_data in rooms[room_code]["players"].items():
                # 각 라운드 결과 가져오기
                rounds_results = player_data.get("rounds_results", {})
                
                # 생존 횟수 계산
                survived_count = 0
                for round_num in range(1, total_rounds + 1):
                    if str(round_num) in rounds_results and rounds_results[str(round_num)]:
                        survived_count += 1
                
                # 사망 횟수 계산        
                died_count = total_rounds - survived_count
                
                # 플레이어 정보 저장
                players_data.append({
                    "name": player_name,
                    "survived_count": survived_count,
                    "died_count": died_count
                })
            
            # 생존 횟수 기준으로 내림차순 정렬
            players_data.sort(key=lambda x: x["survived_count"], reverse=True)
            
            # 순위 부여 및 정렬된 결과 표시
            for i, player in enumerate(players_data, 1):
                player_name = player["name"]
                survived_count = player["survived_count"]
                died_count = player["died_count"]
                
                # 생존/사망 결과를 색상으로 구분하여 표시
                survived_text = f"<span style='color: #00cc00;'>{get_text('survived')}: {survived_count}</span>"
                died_text = f"<span style='color: #ff5555;'>{get_text('died')}: {died_count}</span>"
                
                # 순위 표시와 함께 플레이어 결과 표시
                rank_icon = "🥇" if i == 1 else ("🥈" if i == 2 else ("🥉" if i == 3 else f"{i}."))
                st.markdown(f"{rank_icon} **{player_name}**: {survived_text} | {died_text}", unsafe_allow_html=True)
            
            # 승자 표시 (이미 정렬했으므로 첫 번째 플레이어가 승자)
            if players_data:
                st.markdown("---")
                st.markdown(f"### 🏆 {players_data[0]['name']}")

    st.markdown("---")
    st.info(get_text("restart_info"))
    
    if st.button(get_text("restart")):
        # 언어 설정을 제외한 세션 상태 초기화
        current_language = st.session_state.language
        
        # 방 정보 초기화
        if "room_code" in st.session_state:
            del st.session_state.room_code
        if "player_name" in st.session_state:
            del st.session_state.player_name
        
        # 게임 관련 상태 초기화
        for key in list(st.session_state.keys()):
            if key not in ["language", "page"]:
                del st.session_state[key]
                
        # language 값 복원
        st.session_state.language = current_language
        
        # 시작 페이지로 이동
        st.session_state.page = "start"
        st.rerun()
        
    st.markdown(get_text("thanks"))
    
    # CSS로 시작 화면과 라운드 관련 UI 요소 숨기기
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
