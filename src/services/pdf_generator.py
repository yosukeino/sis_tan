from datetime import datetime


class PDFGenerator:
    def __init__(self):
        with open("src/templates/test_template.html", "r", encoding="utf-8") as f:
            self.template = f.read()
        with open("src/templates/answer_template.html", "r", encoding="utf-8") as f:
            self.answer_template = f.read()

    def create_test(self, df, test_config):
        """テスト用HTMLを生成する"""
        date_str = datetime.now().strftime("%Y%m%d")
        test_number = f"{date_str}001"

        # 問題部分のHTML生成
        questions_html = []
        for i, idx in enumerate(test_config["selected_indices"], 1):
            row = df.iloc[idx - 1]

            if test_config["direction"] == "ja_to_en":
                question = row["訳"]
                if test_config["test_type"] == "partial":
                    # フレーズから単語部分を空欄にする
                    phrase = row["フレーズ"]
                    word = row["単語"]
                    blank_phrase = phrase.replace(word, "(    )")
                    answer_html = f"""
                        <div class="answer-line">
                            <div class="answer-blank">{blank_phrase}</div>
                            <div class="answer-underline"></div>
                        </div>
                    """
                else:
                    answer_html = """
                        <div class="answer-line">
                            <div class="answer-underline"></div>
                        </div>
                    """
            else:
                question = row["フレーズ"]
                if test_config["test_type"] == "partial":
                    answer_html = f"""
                        <div class="answer-line">
                            <div class="answer-blank">{row['和訳問題']}</div>
                            <div class="answer-underline"></div>
                        </div>
                    """
                else:
                    answer_html = """
                        <div class="answer-line">
                            <div class="answer-underline"></div>
                        </div>
                    """

            question_html = f"""
                <div class="question">
                    <div class="question-number">{i}</div>
                    <div class="question-content">
                        <div class="question-text">{question}</div>
                        {answer_html}
                    </div>
                </div>
            """
            questions_html.append(question_html)

        # テンプレートに値を挿入
        html = self.template
        html = html.replace(
            "<!-- RANGE -->", f"{test_config['start_num']}～{test_config['end_num']}"
        )
        html = html.replace("<!-- TEST_NUMBER -->", test_number)
        html = html.replace(
            "<!-- TOTAL_QUESTIONS -->", str(len(test_config["selected_indices"]))
        )
        html = html.replace("<!-- QUESTIONS -->", "\n".join(questions_html))

        return html

    def create_answer(self, df, test_config):
        """解答用HTMLを生成する"""
        date_str = datetime.now().strftime("%Y%m%d")
        test_number = f"{date_str}001"

        questions_html = []
        for i, idx in enumerate(test_config["selected_indices"], 1):
            row = df.iloc[idx - 1]

            if test_config["direction"] == "ja_to_en":
                question = row["訳"]
                if test_config["test_type"] == "partial":
                    # 一部空欄の場合は空欄に入る単語のみを表示
                    answer = row["単語"]
                else:
                    # 全文記入の場合はフレーズ全体を表示
                    answer = row["フレーズ"]
            else:
                question = row["フレーズ"]
                if test_config["test_type"] == "partial":
                    # 日本語の一部空欄の場合（必要に応じて実装）
                    answer = row["訳"]
                else:
                    answer = row["訳"]

            question_html = f"""
                <div class="question">
                    <div class="question-number">{i}</div>
                    <div class="question-content">
                        <div class="question-text">{question}</div>
                        <div class="answer-text">
                            <span class="answer-label">答え: </span>{answer}
                        </div>
                    </div>
                </div>
            """
            questions_html.append(question_html)

        html = self.answer_template
        html = html.replace(
            "<!-- RANGE -->", f"{test_config['start_num']}～{test_config['end_num']}"
        )
        html = html.replace("<!-- TEST_NUMBER -->", test_number)
        html = html.replace("<!-- QUESTIONS -->", "\n".join(questions_html))

        return html
