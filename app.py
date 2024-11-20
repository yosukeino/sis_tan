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

def main():
    """メインアプリケーション"""
    st.title("英単語テストメーカー")
    
    try:
        # データの読み込み
        config = AppConfig()
        df = pd.read_csv(config.get_data_file_path(), encoding=config.ENCODING)
        
        # UIコンポーネントの作成と描画
        form = TestForm(max_range=len(df))
        form_data = form.render()
        
        # テスト作成ボタンの表示と処理
        if form.render_create_button():
            try:
                # 選択された範囲から問題のインデックスを取得
                range_values = form_data['range_values']
                available_indices = list(range(range_values[0], range_values[1] + 1))
                
                # 問題の選択
                num_questions = form_data['num_questions']
                if len(available_indices) > num_questions:
                    selected_indices = random.sample(available_indices, num_questions)
                else:
                    selected_indices = available_indices

                if form_data['random_order']:
                    random.shuffle(selected_indices)
                else:
                    selected_indices.sort()
                
                # テスト設定の作成
                test_config = TestConfig.create_from_form(form_data, selected_indices)
                
                # PDFジェネレーターの作成とHTML生成
                generator = PDFGenerator()
                html_content = generator.create_test(df, test_config.to_dict())

                # ダウンロードリンクの生成
                b64 = base64.b64encode(html_content.encode()).decode()
                st.markdown(
                    f'<a href="data:text/html;base64,{b64}" download="test.html">テストをダウンロード</a>', 
                    unsafe_allow_html=True
                )
                
                # 解答の生成（オプション）
                if form_data['create_answer']:
                    answer_html = generator.create_answer(df, test_config.to_dict())
                    b64_answer = base64.b64encode(answer_html.encode()).decode()
                    st.markdown(
                        f'<a href="data:text/html;base64,{b64_answer}" download="test_answer.html">解答をダウンロード</a>', 
                        unsafe_allow_html=True
                    )
                
                # プレビューの表示
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