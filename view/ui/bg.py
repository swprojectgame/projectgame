import streamlit as st
import uuid

def bg(gif_url: str):
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("{gif_url}");
            background-size: cover; /* 화면에 꽉 차게 */
            background-position: center; /* 이미지가 가운데 오게 */
            background-attachment: fixed; /* 스크롤해도 배경 고정 */
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
def bg_cl():
     st.markdown(
            """
            <style>
            .stApp {
                background-image: none !important;
                background-color: transparent !important;
            }
            </style>
            """,
            unsafe_allow_html=True
    )