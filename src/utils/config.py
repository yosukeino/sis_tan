from pathlib import Path
from typing import Dict, Any
import os
from dotenv import load_dotenv

# .env ファイルの読み込み
load_dotenv()

class AppConfig:
    """アプリケーションの設定を管理するクラス"""
    
    # プロジェクトのルートディレクトリを取得
    ROOT_DIR = Path(__file__).parent.parent.parent
    
    # 問題数の設定
    DEFAULT_QUESTIONS = 20
    MAX_QUESTIONS = 50
    MIN_QUESTIONS = 1
    
    # 問題形式の設定
    DIRECTION_OPTIONS = [
        ('日本語→英語', 'ja_to_en'),
        ('英語→日本語', 'en_to_ja')
    ]
    
    TEST_TYPE_OPTIONS = [
        ('一部空欄', 'partial'),
        ('全文記入', 'full')
    ]
    
    # データファイルの設定
    DATA_DIR = ROOT_DIR / 'data'
    WORD_LIST_PATH = DATA_DIR / 'list.csv'
    ENCODING = 'shift-jis'
    
    # 設定辞書
    DATA_CONFIG = {
        'csv_path': str(WORD_LIST_PATH),
        'encoding': ENCODING,
    }

    TEST_CONFIG = {
        'max_questions': MAX_QUESTIONS,
        'default_questions': DEFAULT_QUESTIONS,
        'min_questions': MIN_QUESTIONS,
    }

    UI_CONFIG = {
        'direction_options': DIRECTION_OPTIONS,
        'test_type_options': TEST_TYPE_OPTIONS
    }
    
    @classmethod
    def get_data_file_path(cls):
        """単語リストファイルのパスを返す"""
        return str(cls.WORD_LIST_PATH)
    
    @classmethod
    def validate_data_file(cls):
        """データファイルの存在を確認"""
        return cls.WORD_LIST_PATH.exists()
    
    @staticmethod
    def get_required_columns():
        """必要なカラムのリストを返す"""
        return ['単語', '意味', 'フレーズ', '訳', '英作問題', '和訳問題']
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """設定を取得する関数"""
        return {
            'data': cls.DATA_CONFIG,
            'test': cls.TEST_CONFIG,
            'ui': cls.UI_CONFIG,
        }

class TestConfig:
    """テスト生成の設定を管理するクラス"""
    
    def __init__(self, range_values, selected_indices, direction, test_type):
        self.start_num = range_values[0]
        self.end_num = range_values[1]
        self.selected_indices = selected_indices
        self.direction = direction[1]  # タプルの2番目の要素（識別子）を使用
        self.test_type = test_type[1]
    
    def to_dict(self):
        """設定を辞書形式で返す"""
        return {
            'start_num': self.start_num,
            'end_num': self.end_num,
            'selected_indices': self.selected_indices,
            'direction': self.direction,
            'test_type': self.test_type
        }

    @classmethod
    def create_from_form(cls, form_data, selected_indices):
        """フォームデータからTestConfigインスタンスを作成"""
        return cls(
            range_values=form_data['range_values'],
            selected_indices=selected_indices,
            direction=form_data['direction'],
            test_type=form_data['test_type']
        )