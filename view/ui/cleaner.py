import streamlit as st

def clean_ui(hide_recommend_button=False):
    """
    게임시작화면에서 보이는 라운드 변경, 게임방법, 게임시작 버튼 등의 요소를
    시나리오와 프롬프트 화면에서 숨기는 CSS를 적용합니다.
    
    Args:
        hide_recommend_button (bool): 추천 시나리오 버튼을 숨길지 여부
    """
    
    # CSS 스타일 정의
    css = """
    <style>
    /* 공통 숨김 처리 스타일 */
    button {
        /* 'submit' 또는 '제출' 텍스트가 포함된 버튼은 예외 처리 */
    }
    
    /* 게임/시작 관련 버튼 숨김 */
    button:not(:contains("submit")):not(:contains("제출")):is(
        :contains("게임"),
        :contains("시작"),
        :contains("Start"),
        :contains("Game"),
        :contains("🚀")
    ),
    div:has(> button:contains("게임")),
    div:has(> button:contains("시작")),
    div:has(> button:contains("Start")),
    div:has(> button:contains("🚀")) {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        opacity: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }

    /* 라운드 관련 숨김 */
    div:has(> *:contains("라운드")),
    div:has(> *:contains("Round")) {
        display: none !important;
    }

    input[type="number"],
    .stNumberInput,
    div:has(> input[type="number"]) {
        display: none !important;
    }
    """

    if not hide_recommend_button:
        css += """
    /* 추천 버튼은 표시 (예외 처리) */
    button:contains("추천"),
    button:contains("Recommend") {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
    }
        """
    else:
        css += """
    /* 추천 버튼 포함 모든 버튼 숨김 */
    button:contains("추천"):not(:contains("submit")):not(:contains("제출")),
    button:contains("Recommend"):not(:contains("submit")):not(:contains("제출")),
    button:contains("recommend"):not(:contains("submit")):not(:contains("제출")),
    button:contains("시나리오"),
    button:contains("Scenario") {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        height: 0 !important;
        width: 0 !important;
        position: absolute !important;
        left: -9999px !important;
    }
        """

    css += "</style>"

    # JS로 submit 버튼 제외하고 삭제
    js = f"""
    <script>
    function removeElements() {{
        const buttons = document.querySelectorAll('button');
        for (let button of buttons) {{
            const text = button.textContent.toLowerCase();
            if (
                (text.includes('게임') || text.includes('start') || text.includes('game') || text.includes('🚀') || text.includes('시작')) &&
                !text.includes('submit') && !text.includes('제출')
            ) {{
                if (button.parentElement) {{
                    button.parentElement.style.display = 'none';
                    button.parentElement.style.visibility = 'hidden';
                    button.parentElement.style.height = '0';
                    button.parentElement.style.opacity = '0';
                }}
                button.style.display = 'none';
                button.style.visibility = 'hidden';
                button.style.height = '0';
                button.style.opacity = '0';
            }}
            
            const isRecommend = text.includes('추천') || text.includes('recommend') || text.includes('scenario') || text.includes('시나리오');
            if (isRecommend && {str(hide_recommend_button).lower()} && !text.includes('submit') && !text.includes('제출')) {{
                if (button.parentElement) {{
                    button.parentElement.style.display = 'none';
                    button.parentElement.style.visibility = 'hidden';
                    button.parentElement.style.height = '0';
                }}
                button.style.display = 'none';
                button.style.visibility = 'hidden';
                button.style.height = '0';
            }}
        }}

        const roundText = ['라운드', 'round'];
        const allElems = document.querySelectorAll('*');
        for (let el of allElems) {{
            const txt = el.textContent.toLowerCase();
            if (roundText.some(keyword => txt.includes(keyword))) {{
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.height = '0';
            }}
        }}

        document.querySelectorAll('input[type="number"]').forEach(input => {{
            const container = input.closest('.element-container');
            if (container) {{
                container.style.display = 'none';
                container.style.height = '0';
                container.style.visibility = 'hidden';
            }}
        }});
    }}

    document.addEventListener('DOMContentLoaded', removeElements);
    const observer = new MutationObserver(removeElements);
    observer.observe(document.body, {{ childList: true, subtree: true }});
    setInterval(removeElements, 200);
    </script>
    """

    st.markdown(css, unsafe_allow_html=True)
    st.markdown(js, unsafe_allow_html=True)
