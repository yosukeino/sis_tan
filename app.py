import streamlit as st
import pandas as pd
import base64
import random
import os
import traceback

from src.utils.config import AppConfig, TestConfig
from src.services.pdf_generator import PDFGenerator
from src.components.test_form import TestForm
from src.components.preview import Preview

# ページ設定
st.set_page_config(page_title="英単語テストメーカー", page_icon="📚", layout="centered")


def load_css():
    """スタイルシートを読み込む"""
    with open("src/styles/main.css", "r", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    """メインアプリケーション"""
    st.markdown(
        '<h1 class="main-title">📚 英単語テストメーカー</h1>', unsafe_allow_html=True
    )

    try:
        # データの読み込み
        config = AppConfig()
        df = pd.read_csv(config.get_data_file_path(), encoding=config.ENCODING)

        # UIコンポーネントをカード内に配置
        st.markdown('<div class="styledbox">', unsafe_allow_html=True)

        # UIコンポーネントの配置
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("### 📋 テスト設定")
            # 問題範囲選択
            max_range = len(df)
            range_values = st.slider(
                "出題範囲を選択", 1, max_range, (1, 20), key="range_slider"
            )

            # 出題数選択
            num_questions = st.number_input(
                "出題数", min_value=1, max_value=50, value=20, key="num_questions"
            )

        with col2:
            st.markdown("### 🎯 出題形式")
            # 問題形式選択
            direction = st.radio(
                "問題形式",
                options=[("日本語→英語", "ja_to_en"), ("英語→日本語", "en_to_ja")],
                format_func=lambda x: x[0],
                key="direction",
            )

            # テストタイプ選択
            test_type = st.radio(
                "解答形式",
                options=[("一部空欄", "partial"), ("全文記入", "full")],
                format_func=lambda x: x[0],
                key="test_type",
            )

            st.markdown("### ⚙️ その他の設定")
            # 問題順序選択
            random_order = st.checkbox("ランダムに問題を並べ替え", key="random_order")

            # 答え作成オプション
            create_answer = st.checkbox("答えも合わせて作成する", key="create_answer")

        st.markdown("</div>", unsafe_allow_html=True)

        # テスト作成ボタン
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button(
                "テストを作成する", key="create_test_button", use_container_width=True
            ):
                try:
                    # 選択された範囲から問題のインデックスを取得
                    available_indices = list(
                        range(range_values[0], range_values[1] + 1)
                    )

                    # 問題の選択
                    if len(available_indices) > num_questions:
                        selected_indices = random.sample(
                            available_indices, num_questions
                        )
                    else:
                        selected_indices = available_indices

                    if random_order:
                        random.shuffle(selected_indices)
                    else:
                        selected_indices.sort()

                    # テスト設定の作成
                    test_config = TestConfig.create_from_form(
                        {
                            "range_values": range_values,
                            "num_questions": num_questions,
                            "direction": direction,
                            "test_type": test_type,
                            "random_order": random_order,
                            "create_answer": create_answer,
                        },
                        selected_indices,
                    )

                    # PDFジェネレーターの作成とHTML生成
                    generator = PDFGenerator()
                    html_content = generator.create_test(df, test_config.to_dict())

                    # ダウンロードリンクの生成
                    st.markdown('<div class="styledbox">', unsafe_allow_html=True)
                    b64 = base64.b64encode(html_content.encode()).decode()
                    st.markdown(
                        f'<a href="data:text/html;base64,{b64}" download="test.html">テストをダウンロード</a>',
                        unsafe_allow_html=True,
                    )

                    # 解答の生成（オプション）
                    if create_answer:
                        answer_html = generator.create_answer(df, test_config.to_dict())
                        b64_answer = base64.b64encode(answer_html.encode()).decode()
                        st.markdown(
                            f'<a href="data:text/html;base64,{b64_answer}" download="test_answer.html">解答をダウンロード</a>',
                            unsafe_allow_html=True,
                        )
                    st.markdown("</div>", unsafe_allow_html=True)

                    # プレビューの表示
                    st.markdown("### 📄 プレビュー")
                    Preview.render_html(html_content)

                except Exception as e:
                    st.error(f"テスト生成中にエラーが発生しました: {e}")
                    st.write("現在のディレクトリ:", os.getcwd())
                    st.write("data/の内容:", os.listdir("data"))

    except Exception as e:
        st.error(f"データファイルの読み込みに失敗しました: {e}")
        st.write("現在のディレクトリ:", os.getcwd())
        st.write("data/の内容:", os.listdir("data"))


if __name__ == "__main__":
    main()
