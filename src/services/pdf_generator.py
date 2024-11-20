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
                    answer_format = row['英作問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
                    answer_class = 'answer-space partial'
                else:
                    answer_format = '___________________________'
                    answer_class = 'answer-space'
            else:
                question = row['フレーズ']
                if test_config['test_type'] == 'partial':
                    answer_format = row['和訳問題'].replace('(', '(&nbsp;&nbsp;&nbsp;&nbsp;').replace(')', '&nbsp;&nbsp;&nbsp;&nbsp;)')
                    answer_class = 'answer-space partial'
                else:
                    answer_format = '___________________________'
                    answer_class = 'answer-space'
                    
            problems_html += f"""
                <div class="problem-row">
                    <div class="number">{i}</div>
                    <div class="question">{question}</div>
                    <div class="{answer_class}">{answer_format}</div>
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
                        margin: 1.5cm;
                    }}
                    body {{
                        font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
                        margin: 0;
                        padding: 15px;
                        line-height: 1.4;
                    }}
                    .container {{
                        background: white;
                        padding: 15px;
                    }}
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-start;
                        margin-bottom: 20px;
                        border-bottom: 2px solid #f0f0f0;
                        padding-bottom: 15px;
                    }}
                    .title-section {{
                        flex: 2;
                    }}
                    .test-title {{
                        font-size: 20px;
                        font-weight: bold;
                        margin-bottom: 8px;
                    }}
                    .test-info {{
                        font-size: 13px;
                        color: #666;
                    }}
                    .test-number {{
                        color: #888;
                        font-size: 11px;
                    }}
                    .name-section {{
                        flex: 1;
                        text-align: right;
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                    }}
                    .name-field {{
                        border: 2px solid #e0e0e0;
                        border-radius: 6px;
                        padding: 10px 20px;
                        min-width: 200px;
                        min-height: 20px;
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
                        font-size: 12px;
                    }}
                    .score-field {{
                        border: 2px solid #e0e0e0;
                        border-radius: 6px;
                        padding: 10px 20px;
                        min-width: 120px;
                        min-height: 20px;
                        position: relative;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                    }}
                    .score-field:before {{
                        content: '得点';
                        position: absolute;
                        top: -10px;
                        left: 10px;
                        background: white;
                        padding: 0 5px;
                        color: #666;
                        font-size: 12px;
                    }}
                    .score-field .total {{
                        margin-left: 5px;
                        color: #666;
                    }}
                    .problems-container {{
                        display: flex;
                        flex-direction: column;
                        gap: 12px;
                    }}
                    .problem-row {{
                        display: grid;
                        grid-template-columns: 40px 0.6fr 1.4fr;
                        gap: 15px;
                        align-items: center;
                        margin-bottom: 8px;
                        min-height: 40px;
                    }}
                    .number {{
                        width: 28px;
                        height: 28px;
                        background: #f8f9fa;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        color: #2c3e50;
                        font-size: 13px;
                    }}
                    .question {{
                        font-size: 13px;
                        padding: 6px 12px;
                        background: #f8f9fa;
                        border-radius: 4px;
                        line-height: 1.4;
                    }}
                    .answer-space {{
                        min-height: 35px;
                        padding: 6px 10px;
                        margin: 3px 0;
                        border: none;
                        border-bottom: 2px solid #666;
                        background-color: #f8f9fa;
                        width: 100%;
                        box-sizing: border-box;
                        line-height: 1.6;
                        font-size: 14px;
                    }}
                    @media print {{
                        .answer-space {{
                            background-color: transparent;
                            min-height: 32px;
                            border-bottom: 1px solid #000;
                        }}
                        .problem-row {{
                            page-break-inside: avoid;
                        }}
                        .problems-container {{
                            max-height: 297mm;
                            column-gap: 0;
                        }}
                    }}
                    .answer-space.partial {{
                        font-family: "Courier New", monospace;
                        letter-spacing: 0.1em;
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
                            <div class="score-field">_____<span class="total">/{len(test_config['selected_indices'])}</span></div>
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
                        margin: 1.5cm;
                    }}
                    body {{
                        font-family: "Helvetica Neue", Arial, "Hiragino Kaku Gothic ProN", "Hiragino Sans", Meiryo, sans-serif;
                        margin: 0;
                        padding: 15px;
                        line-height: 1.4;
                    }}
                    .container {{
                        background: white;
                        padding: 15px;
                    }}
                    .header {{
                        display: flex;
                        justify-content: space-between;
                        align-items: flex-start;
                        margin-bottom: 20px;
                        border-bottom: 2px solid #f0f0f0;
                        padding-bottom: 15px;
                    }}
                    .title-section {{
                        flex: 2;
                    }}
                    .test-title {{
                        font-size: 20px;
                        font-weight: bold;
                        margin-bottom: 8px;
                    }}
                    .test-info {{
                        font-size: 13px;
                        color: #666;
                    }}
                    .test-number {{
                        color: #888;
                        font-size: 11px;
                    }}
                    .problems-container {{
                        display: flex;
                        flex-direction: column;
                        gap: 12px;
                    }}
                    .problem-row {{
                        display: grid;
                        grid-template-columns: 40px 1fr;
                        gap: 15px;
                        align-items: center;
                        margin-bottom: 8px;
                        min-height: 40px;
                    }}
                    .number {{
                        width: 28px;
                        height: 28px;
                        background: #f8f9fa;
                        border-radius: 50%;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-weight: bold;
                        color: #2c3e50;
                        font-size: 13px;
                    }}
                    .question {{
                        font-size: 13px;
                        padding: 6px 12px;
                        background: #f8f9fa;
                        border-radius: 4px;
                        line-height: 1.4;
                    }}
                    .answer {{
                        color: #D63230;
                        font-weight: bold;
                        margin-top: 5px;
                        font-size: 13px;
                    }}
                    .answer-label {{
                        color: #2c3e50;
                        font-size: 11px;
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