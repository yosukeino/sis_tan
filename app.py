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
st.set_page_config(
    page_title="英単語テストメーカー",
    page_icon="📚",
    layout="centered"
)

# カスタムCSS
st.markdown("""
<style>
    /* メインコンテナのスタイル */
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
        background-color: #FFF4B7;
        background: linear-gradient(135deg, #FFF4B7 0%, #fff 100%);
    }
    
    /* タイトルのスタイル */
    .main-title {
        color: #000B58;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 2rem;
        text-align: center;
        padding: 1rem;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* カード風のコンテナ */
    .styledbox {
        padding: 25px;
        border-radius: 15px;
        background: white;
        box-shadow: 0 4px 15px rgba(0, 11, 88, 0.1);
        margin-bottom: 25px;
        border: 1px solid rgba(0, 49, 97, 0.1);
    }
    
    /* セクションタイトル */
    h3 {
        color: #003161 !important;
        font-weight: 600 !important;
        margin-bottom: 1.5rem !important;
    }
    
    /* スライダーのスタイル */
    .stSlider > div > div > div {
        background-color: #006A67 !important;
    }
    
    /* ラジオボタンのスタイル */
    .stRadio > label {
        background-color: #fff;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
        transition: all 0.2s;
        border: 1px solid rgba(0, 106, 103, 0.2);
    }
    .stRadio > label:hover {
        background-color: rgba(0, 106, 103, 0.05);
        border-color: #006A67;
    }
    
    /* チェックボックスのスタイル */
    .stCheckbox > label {
        background-color: #fff;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
        border: 1px solid rgba(0, 106, 103, 0.2);
        transition: all 0.2s;
    }
    .stCheckbox > label:hover {
        background-color: rgba(0, 106, 103, 0.05);
        border-color: #006A67;
    }
    
    /* 数値入力のスタイル */
    .stNumberInput > div > div > input {
        border-color: rgba(0, 106, 103, 0.2);
    }
    
    /* ボタンのスタイル */
    .stButton > button {
        background: linear-gradient(135deg, #003161 0%, #006A67 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 4px 6px rgba(0, 11, 88, 0.1);
    }
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 8px rgba(0, 11, 88, 0.2);
        background: linear-gradient(135deg, #000B58 0%, #003161 100%);
    }
    
    /* ダウンロードリンクのスタイル */
    a {
        color: #006A67 !important;
        text-decoration: none;
        padding: 8px 16px;
        border-radius: 6px;
        transition: all 0.2s;
        display: inline-block;
        margin: 5px 0;
        border: 1px solid #006A67;
    }
    a:hover {
        background-color: #006A67;
        color: white !important;
    }
    
    /* 区切り線のスタイル */
    hr {
        border-color: rgba(0, 11, 88, 0.1);
        margin: 2rem 0;
    }
    
    /* エラーメッセージのスタイル */
    .stAlert {
        background-color: rgba(255, 244, 183, 0.5);
        color: #000B58;
        border-color: #000B58;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """メインアプリケーション"""
    st.markdown('<h1 class="main-title">📚 英単語テストメーカー</h1>', unsafe_allow_html=True)
    
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
                "出題範囲を選択",
                1, max_range, (1, 20),
                key="range_slider"
            )
            
            # 出題数選択
            num_questions = st.number_input(
                "出題数",
                min_value=1,
                max_value=50,
                value=20,
                key="num_questions"
            )
        
        with col2:
            st.markdown("### 🎯 出題形式")
            # 問題形式選択
            direction = st.radio(
                "問題形式",
                options=[
                    ('日本語→英語', 'ja_to_en'),
                    ('英語→日本語', 'en_to_ja')
                ],
                format_func=lambda x: x[0],
                key="direction"
            )
            
            # テストタイプ選択
            test_type = st.radio(
                "解答形式",
                options=[
                    ('一部空欄', 'partial'),
                    ('全文記入', 'full')
                ],
                format_func=lambda x: x[0],
                key="test_type"
            )
            
            st.markdown("### ⚙️ その他の設定")
            # 問題順序選択
            random_order = st.checkbox(
                "ランダムに問題を並べ替え",
                key="random_order"
            )
            
            # 答え作成オプション
            create_answer = st.checkbox(
                "答えも合わせて作成する",
                key="create_answer"
            )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # テスト作成ボタン
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("テストを作成する", key="create_test_button", use_container_width=True):
                try:
                    # 選択された範囲から問題のインデックスを取得
                    available_indices = list(range(range_values[0], range_values[1] + 1))
                    
                    # 問題の選択
                    if len(available_indices) > num_questions:
                        selected_indices = random.sample(available_indices, num_questions)
                    else:
                        selected_indices = available_indices

                    if random_order:
                        random.shuffle(selected_indices)
                    else:
                        selected_indices.sort()
                    
                    # テスト設定の作成
                    test_config = TestConfig.create_from_form({
                        'range_values': range_values,
                        'num_questions': num_questions,
                        'direction': direction,
                        'test_type': test_type,
                        'random_order': random_order,
                        'create_answer': create_answer
                    }, selected_indices)
                    
                    # PDFジェネレーターの作成とHTML生成
                    generator = PDFGenerator()
                    html_content = generator.create_test(df, test_config.to_dict())

                    # ダウンロードリンクの生成
                    st.markdown('<div class="styledbox">', unsafe_allow_html=True)
                    b64 = base64.b64encode(html_content.encode()).decode()
                    st.markdown(
                        f'<a href="data:text/html;base64,{b64}" download="test.html">テストをダウンロード</a>', 
                        unsafe_allow_html=True
                    )
                    
                    # 解答の生成（オプション）
                    if create_answer:
                        answer_html = generator.create_answer(df, test_config.to_dict())
                        b64_answer = base64.b64encode(answer_html.encode()).decode()
                        st.markdown(
                            f'<a href="data:text/html;base64,{b64_answer}" download="test_answer.html">解答をダウンロード</a>', 
                            unsafe_allow_html=True
                        )
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # プレビューの表示
                    st.markdown("### 📄 プレビュー")
                    Preview.render_html(html_content)

                except Exception as e:
                    st.error(f"テスト生成中にエラーが発生しました: {e}")
                    st.write("現在のディレクトリ:", os.getcwd())
                    st.write("data/の内容:", os.listdir('data'))

    except Exception as e:
        st.error(f"データファイルの読み込みに失敗しました: {e}")
        st.write("現在のディレクトリ:", os.getcwd())
        st.write("data/の内容:", os.listdir('data'))

if __name__ == "__main__":
    main()