import streamlit as st

class TestForm:
    def __init__(self, max_range):
        """
        テストフォームの初期化
        
        Args:
            max_range (int): 問題範囲の最大値
        """
        self.max_range = max_range
        self.col1, self.col2 = st.columns(2)

    def render(self):
        """
        フォームを描画し、ユーザーの入力を返す
        
        Returns:
            dict: フォームの入力値
        """
        with self.col1:
            range_values = self._render_range_selector()
            num_questions = self._render_question_count()

        with self.col2:
            direction = self._render_direction_selector()
            test_type = self._render_test_type_selector()
            random_order = self._render_random_checkbox()
            create_answer = self._render_answer_checkbox()

        return {
            'range_values': range_values,
            'num_questions': num_questions,
            'direction': direction,
            'test_type': test_type,
            'random_order': random_order,
            'create_answer': create_answer
        }

    def _render_range_selector(self):
        """問題範囲選択スライダーを描画"""
        return st.slider(
            "出題範囲を選択",
            1, self.max_range, (1, 20),
            key="range_slider"
        )

    def _render_question_count(self):
        """出題数入力フィールドを描画"""
        return st.number_input(
            "出題数",
            min_value=1,
            max_value=50,
            value=20,
            key="num_questions"
        )

    def _render_direction_selector(self):
        """問題形式選択ラジオボタンを描画"""
        return st.radio(
            "問題形式",
            options=[
                ('日本語→英語', 'ja_to_en'),
                ('英語→日本語', 'en_to_ja')
            ],
            format_func=lambda x: x[0],
            key="direction"
        )

    def _render_test_type_selector(self):
        """解答形式選択ラジオボタンを描画"""
        return st.radio(
            "解答形式",
            options=[
                ('一部空欄', 'partial'),
                ('全文記入', 'full')
            ],
            format_func=lambda x: x[0],
            key="test_type"
        )

    def _render_random_checkbox(self):
        """ランダム出題チェックボックスを描画"""
        return st.checkbox(
            "ランダムに問題を並べ替え",
            key="random_order"
        )

    def _render_answer_checkbox(self):
        """解答作成チェックボックスを描画"""
        return st.checkbox(
            "答えも合わせて作成する",
            key="create_answer"
        )

    def render_create_button(self):
        """テスト作成ボタンを描画"""
        st.markdown("---")
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            return st.button(
                "テスト作成",
                key="create_test_button",
                use_container_width=True
            )