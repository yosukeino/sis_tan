import streamlit as st


class Preview:
    @staticmethod
    def render_html(html_content: str):
        """HTMLコンテンツをプレビュー表示する

        Args:
            html_content (str): 表示するHTMLコンテンツ
        """
        st.markdown('<div class="styledbox">', unsafe_allow_html=True)
        st.markdown("### 📄 プレビュー", unsafe_allow_html=True)
        st.components.v1.html(html_content, height=600, scrolling=True)
        st.markdown("</div>", unsafe_allow_html=True)
