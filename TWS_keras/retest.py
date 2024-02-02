import pandas as pd
import numpy as np
import copy


"""
預測值回測績效設計區
根據自己策略寫一套回測
"""

class StockRetest:
    def __init__(self) -> None:
        pass


    # keras預測資料 5%停利或是5天賣出回測 回傳最大績效與其二分值 但最後五筆測不到
    def get_binary_value_and_performance(self, df) -> tuple:
        df = copy.deepcopy(df)
        binary_performence_list = []
        for i in range(0, 101):
            binary_num = i/100
            df['binary_prediction'] = (df['prediction'] >= binary_num).astype(int)
            performence_collect = []
            for idx in range(len(df)-5):
                if df['binary_prediction'][idx] == 1:
                    buy_price = df['open'][idx+1]
                    high_price = max(df['high'].loc[idx+1: idx+5])
                    end_sell_price = df['close'][idx+5]
                    high_performence = (high_price - buy_price)/buy_price
                    end_sell_performence = (end_sell_price - buy_price)/buy_price
                    performence_collect.append(0.05 if high_performence > 0.05 else end_sell_performence)
            if performence_collect:
                binary_performence_list.append((binary_num, sum(performence_collect)))
             
        return max(binary_performence_list, key=lambda x:x[1])
    
    # svc預測資料 5%停利或是5天賣出回測 回傳交易次數和最大績效 但最後五筆測不到
    def strategy_retest(self, df, prediction_column) -> tuple:
        df = copy.deepcopy(df)
        performence_collect = []
        for idx in range(len(df)-5):
            if df[prediction_column][idx] == 1:
                buy_price = df['open'][idx+1]
                high_price = max(df['high'].loc[idx+1: idx+5])
                end_sell_price = df['close'][idx+5]
                high_performence = (high_price - buy_price)/buy_price
                end_sell_performence = (end_sell_price - buy_price)/buy_price
                performence_collect.append(buy_price*1000 * 0.05 if high_performence > 0.05 else buy_price*1000*end_sell_performence)
        return len(performence_collect), np.sum(performence_collect)
    

    def strategy_buy_sell_index(self, df, prediction_column) -> list[tuple]:
        df = copy.deepcopy(df)
        buy_idx_list = []
        buy_price_list = []
        sell_idx_list = []
        sell_price_list = []     
        for idx in range(len(df)-5):
            if df[prediction_column][idx] == 1:
                buy_price = df['close'][idx]
                high_price = max(df['high'].loc[idx+1: idx+5])
                high_idx = (df['high'].loc[idx+1: idx+5]).idxmax()
                end_sell_price = df['close'][idx+5]
                end_sell_idx = idx + 5
                high_performence = (high_price - buy_price)/buy_price
                buy_idx_list.append(idx)
                buy_price_list.append(buy_price)
                sell_idx_list.append(high_idx if high_performence > 0.05 else end_sell_idx)
                sell_price_list.append(high_price if high_performence > 0.05 else end_sell_price)  
        return [buy_idx_list, buy_price_list, sell_idx_list, sell_price_list]
    

    def buy_point_decrease(self, df, prediction_column) -> None:
        for i in range(len(df)-4):
            if df.loc[i, prediction_column] == 1:
                df.loc[i+1: i+5, prediction_column] = 0


    def similar_binary(self, df, prediction_column='prediction', target_column='target'):
        df = copy.deepcopy(df)
        # df.dropna(inplace=True)
        binary_similar_list = []
        for i in range(101):
            binary_num = i/100
            df['binary_prediction'] = (df[prediction_column] >= binary_num).astype(int)
            df['similar'] = (df[target_column] == df['binary_prediction']).astype(int)
            binary_similar_list.append((binary_num, np.sum(df['similar'].values)))
        return max(binary_similar_list, key=lambda x:x[1])