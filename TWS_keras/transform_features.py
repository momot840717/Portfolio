from sklearn.preprocessing import StandardScaler
import pandas as pd
import copy

"""
特徵工程函數設計區
"""

class TransformFeatures:
    def __init__(self) -> None:
        self.scaler = StandardScaler()


    def remove_previous_days_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """ 技術指標在表格開頭會有空值跟誤差, 需要移除以減少誤差

        Args:
            df (pd.DataFrame): 

        Returns:
            pd.DataFrame: 
        """
        df = copy.deepcopy(df)
        return df[90:].reset_index(drop=True)
    

    def data_scaler(self, df, n):
        # 選取標準化範圍, 使用前請將表格文字類往左放, 數值往右放
        return self.scaler.fit_transform(df.iloc[:, n:])
    

    def get_target(self, df) -> None:
        # 找特徵目標, 不多做說明訓練答案是甚麼
        # 可以自行變更自己想要找的答案設計
        max_high = df['high'].shift(-1).rolling(window=5, min_periods=1).max().shift(-4)
        df['target'] = (max_high - df['close']) / df['close']
        # df.to_csv('target.csv')
        df.dropna(inplace=True)
        df['target'] = (df['target'] > 0.055).astype(int)


    def data_change(self, df, column_name) -> None:
        # 計算指定資料每日變化量
        df[f'{column_name}_change'] = df[column_name] - df[column_name].shift(1)
