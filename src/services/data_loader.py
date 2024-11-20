import pandas as pd
from typing import Optional
import streamlit as st
from ..utils.config import get_config


class DataLoadError(Exception):
    """データ読み込み時のエラーを処理するカスタム例外"""
    pass

class DataLoader:
    """データ読み込みを担当するクラス"""
    
    @staticmethod
    @st.cache_data  # Streamlitのキャッシュ機能を使用
    def load_wordlist() -> Optional[pd.DataFrame]:
        """
        単語リストを読み込む
        
        Returns:
            Optional[pd.DataFrame]: 読み込んだデータフレーム。エラー時はNone
        """
        config = get_config()
        try:
            df = pd.read_csv(
                config['data']['csv_path'],
                encoding=config['data']['encoding']
            )
            return df
        except Exception as e:
            raise DataLoadError(f"データファイルの読み込みに失敗しました: {e}")
    
    @staticmethod
    def validate_data(df: pd.DataFrame) -> bool:
        """
        データフレームの妥当性をチェック
        
        Args:
            df (pd.DataFrame): チェックするデータフレーム
            
        Returns:
            bool: データが妥当な場合True
        """
        required_columns = ['単語', '意味', 'フレーズ', '訳', '英作問題', '和訳問題']
        return all(col in df.columns for col in required_columns)