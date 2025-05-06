#result.py 이후로 나오는 게임 종료 화면
import streamlit as st
from view.ui.bg import bg  # 배경 유지

def a6():
    bg()
    st.title("🏁 게임 종료")

    st.success("모든 라운드가 종료되었습니다!")
    st.markdown("### 🎉 생존과 죽음의 AI 게임이 끝났습니다.")

    st.markdown("---")
    st.info("🔁 다시 시작하려면 브라우저를 새로고침하거나, 왼쪽 메뉴에서 '처음'으로 돌아가세요.")
    st.markdown("감사합니다! 😊")