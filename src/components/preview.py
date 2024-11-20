import streamlit as st

class Preview:
    """プレビュー表示を管理するクラス"""
    
    @staticmethod
    def render_html(html_content: str, height: int = 600):
        """HTMLコンテンツをプレビュー表示する"""
        st.markdown("### プレビュー")
        st.components.v1.html(html_content, height=height)