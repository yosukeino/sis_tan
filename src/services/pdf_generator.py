from datetime import datetime

class PDFGenerator:
    def __init__(self):
        pass

    def create_test(self, df, test_config):
        """テスト用HTMLを生成する"""
        date_str = datetime.now().strftime('%Y%m%d')
        test_number = f"{date_str}001"
        
        # 問題部分のHTML生成
        problems_html = ""
        for i, idx in enumerate(test_config['selected_indices'], 1):
            row = df.iloc[idx - 1]
            
            if test_config['direction'] == 'ja_to_en':
                question = row['訳']
                if test_config['test_type'] == 'partial':
                    answer = row['英作問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
                else:
                    answer = '___________________________'
            else:
                question = row['フレーズ']
                if test_config['test_type'] == 'partial':
                    answer = row['和訳問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
                else:
                    answer = '___________________________'
                    
            problems_html += f"""
                <div class="problem-row">
                    <div class="number">{i}</div>
                    <div class="question">{question}</div>
                    <div class="answer-space">{answer}</div>
                </div>
            """
        
        # 完全なHTMLの生成
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        size: A4;
                        margin: 2cm;
                    }}
                    body {{
                        font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        background: white;
                        padding: 20px;
                    }}
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-start;
                        margin-bottom: 30px;
                        border-bottom: 2px solid #f0f0f0;
                        padding-bottom: 20px;
                    }}
                    .title-section {{
                        flex: 2;
                    }}
                    .test-title {{
                        font-size: 24px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }}
                    .test-info {{
                        font-size: 14px;
                        color: #666;
                    }}
                    .test-number {{
                        color: #888;
                        font-size: 12px;
                    }}
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
                    .problems-container {{
                        display: flex;
                        flex-direction: column;
                        gap: 20px;
                    }}
                    .problem-row {{
                        display: grid;
                        grid-template-columns: 40px 0.8fr 1.2fr;
                        gap: 20px;
                        align-items: center;
                    }}
                    .number {{
                        width: 32px;
                        height: 32px;
                        background: #f8f9fa;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        color: #2c3e50;
                    }}
                    .question {{
                        font-size: 14px;
                        padding: 8px 15px;
                        background: #f8f9fa;
                        border-radius: 4px;
                        line-height: 1.5;
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
                            <div class="test-info">出題範囲: {test_config['start_num']}～{test_config['end_num']}</div>
                            <div class="test-number">テスト番号: {test_number}</div>
                        </div>
                        <div class="name-section">
                            <div class="name-field"></div>
                        </div>
                    </div>
                    <div class="problems-container">
                        {problems_html}
                    </div>
                </div>
            </body>
            </html>
        """

    def create_answer(self, df, test_config):
        """解答用HTMLを生成する"""
        date_str = datetime.now().strftime('%Y%m%d')
        test_number = f"{date_str}001"
        
        # 問題と解答のHTML生成
        problems_html = ""
        for i, idx in enumerate(test_config['selected_indices'], 1):
            row = df.iloc[idx - 1]
            
            if test_config['direction'] == 'ja_to_en':
                question = row['訳']
                answer = row['フレーズ']
            else:
                question = row['フレーズ']
                answer = row['訳']
                
            problems_html += f"""
                <div class="problem-row">
                    <div class="number">{i}</div>
                    <div class="question">
                        {question}
                        <div class="answer">
                            <span class="answer-label">答え:</span>{answer}
                        </div>
                    </div>
                </div>
            """
        
        # 完全なHTMLの生成
        return f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="UTF-8">
                <style>
                    @page {{
                        size: A4;
                        margin: 2cm;
                    }}
                    body {{
                        font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
                        margin: 0;
                        padding: 20px;
                    }}
                    .container {{
                        background: white;
                        padding: 20px;
                    }}
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-start;
                        margin-bottom: 30px;
                        border-bottom: 2px solid #f0f0f0;
                        padding-bottom: 20px;
                    }}
                    .title-section {{
                        flex: 2;
                    }}
                    .test-title {{
                        font-size: 24px;
                        font-weight: bold;
                        margin-bottom: 10px;
                    }}
                    .test-info {{
                        font-size: 14px;
                        color: #666;
                    }}
                    .test-number {{
                        color: #888;
                        font-size: 12px;
                    }}
                    .problems-container {{
                        display: flex;
                        flex-direction: column;
                        gap: 20px;
                    }}
                    .problem-row {{
                        display: grid;
                        grid-template-columns: 40px 1fr;
                        gap: 20px;
                        align-items: center;
                    }}
                    .number {{
                        width: 32px;
                        height: 32px;
                        background: #f8f9fa;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        color: #2c3e50;
                    }}
                    .question {{
                        font-size: 14px;
                        padding: 8px 15px;
                        background: #f8f9fa;
                        border-radius: 4px;
                        line-height: 1.5;
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
                            <div class="test-info">出題範囲: {test_config['start_num']}～{test_config['end_num']}</div>
                            <div class="test-number">テスト番号: {test_number}</div>
                        </div>
                    </div>
                    <div class="problems-container">
                        {problems_html}
                    </div>
                </div>
            </body>
            </html>
        """