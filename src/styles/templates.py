class TestTemplates:
    @staticmethod
    def get_base_styles():
        """共通のCSSスタイルを返す"""
        return """
            @page {
                size: A4;
                margin: 2cm;
            }
            body {
                font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
                margin: 0;
                padding: 20px;
            }
            .container {
                background: white;
                padding: 20px;
            }
            .header {
                display: flex;
                justify-content: space-between;
                align-items: flex-start;
                margin-bottom: 30px;
                border-bottom: 2px solid #f0f0f0;
                padding-bottom: 20px;
            }
            .title-section {
                flex: 2;
            }
            .test-title {
                font-size: 24px;
                font-weight: bold;
                margin-bottom: 10px;
            }
            .test-info {
                font-size: 14px;
                color: #666;
            }
            .test-number {
                color: #888;
                font-size: 12px;
            }
            .problems-container {
                display: flex;
                flex-direction: column;
                gap: 20px;
            }
            .problem-row {
                display: grid;
                gap: 20px;
                align-items: center;
            }
            .number {
                width: 32px;
                height: 32px;
                background: #f8f9fa;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: #2c3e50;
            }
            .question {
                font-size: 14px;
                padding: 8px 15px;
                background: #f8f9fa;
                border-radius: 4px;
                line-height: 1.5;
            }
        """

    @staticmethod
    def get_test_template():
        """テスト用のHTMLテンプレートを返す"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {TestTemplates.get_base_styles()}
                .name-section {{
                    flex: 1;
                    text-align: right;
                }}
                .name-field {{
                    border: 2px solid #e0e0e0;
                    border-radius: 6px;
                    padding: 12px 25px;
                    min-width: 250px;
                    min-height: 25px;
                    position: relative;
                    margin-top: 20px;
                }}
                .name-field:before {{
                    content: '氏名';
                    position: absolute;
                    top: -10px;
                    left: 10px;
                    background: white;
                    padding: 0 5px;
                    color: #666;
                    font-size: 14px;
                }}
                .problem-row {{
                    grid-template-columns: 40px 0.8fr 1.2fr;
                }}
                .answer-space {{
                    border-bottom: 2px solid #e0e0e0;
                    min-height: 35px;
                    font-size: 16px;
                    padding: 5px 0;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="title-section">
                        <div class="test-title">英単語テスト</div>
                        <div class="test-info">出題範囲: {{start_num}}～{{end_num}}</div>
                        <div class="test-number">テスト番号: {{test_number}}</div>
                    </div>
                    <div class="name-section">
                        <div class="name-field"></div>
                    </div>
                </div>
                <div class="problems-container">
                    {{problems}}
                </div>
            </div>
        </body>
        </html>
        """

    @staticmethod
    def get_answer_template():
        """解答用のHTMLテンプレートを返す"""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <style>
                {TestTemplates.get_base_styles()}
                .problem-row {{
                    grid-template-columns: 40px 1fr;
                }}
                .answer {{
                    color: #D63230;
                    font-weight: bold;
                    margin-top: 5px;
                    font-size: 14px;
                }}
                .answer-label {{
                    color: #2c3e50;
                    font-size: 12px;
                    margin-right: 5px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <div class="title-section">
                        <div class="test-title">英単語テスト（解答）</div>
                        <div class="test-info">出題範囲: {{start_num}}～{{end_num}}</div>
                        <div class="test-number">テスト番号: {{test_number}}</div>
                    </div>
                </div>
                <div class="problems-container">
                    {{problems}}
                </div>
            </div>
        </body>
        </html>
        """