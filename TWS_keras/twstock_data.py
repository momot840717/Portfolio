import twstock as ts
import pandas as pd
from Indicators_cal import Indicators
from transform_features import TransformFeatures
from stock_ml import StockML
from retest import StockRetest
from datetime import datetime, timedelta
import time

def main():
    stock_code = '2329'
    ts_data = ts.Stock(stock_code)
    now = time.time()
    history_ts_data = ts_data.fetch_from(2018, 1)
    print(f"Time of getting history data: {time.time()-now}")

    # 選擇我要的表格欄位
    ts_df = pd.DataFrame(history_ts_data)[['date', 'open', 'high', 'low', 'close', 'capacity', 'change']]
    # print(ts_df)
    id_cal = Indicators()
    close_price = ts_df['close']
    high_price = ts_df['high']
    low_price = ts_df['low']

    ts_df['RSI6'] = id_cal.cal_rsi(close_price)
    ts_df['DIF'], ts_df['MACD'], ts_df['OSC'] = id_cal.cal_macd(close_price)
    ts_df['K'], ts_df['D'], ts_df['J'] = id_cal.cal_kdj(close_price, high_price, low_price)
    ts_df['close - MA10'] = close_price - id_cal.cal_ma(close_price, 10)
    # print(ts_df)

    trans = TransformFeatures()

    trans.data_change(ts_df, 'capacity')
    
    trans_df = trans.remove_previous_days_data(ts_df)
    column_index = 6
    trans_df.iloc[:, column_index:] = trans.data_scaler(trans_df, column_index)
    trans.get_target(trans_df)
    # trans_df = trans_df[trans_df['date']<'2023-01-16']
    # trans_df.to_csv(f'trans_df_{stock_code}.csv')

    columns_to_remove = [
        'open', 
        'high', 
        'low',
        'close',
        'capacity',
        'change',
        ]
    drop_trans_df = trans_df.drop(columns=columns_to_remove)
    
    stock_ml = StockML()
    retest = StockRetest()
    return_days = 300
    test_prediction_list = []
    df_size = len(trans_df)
    trans_df['prediction'] = pd.Series()
    trans_df['iterated_prediction'] = pd.Series()
    time_steps = 5
    for i in range(return_days):
        feature_train_df = drop_trans_df.iloc[:df_size-return_days+i, 1:]
        feature_test_df = drop_trans_df.iloc[df_size-return_days+i-4: df_size-return_days+i+1, 1:]
        model = stock_ml.lstm_model(feature_train_df, time_steps=time_steps)
        trans_df.loc[time_steps-1: len(trans_df)-return_days+i-1, 'prediction'] = stock_ml.lstm_predict(model, feature_train_df, time_steps=time_steps)
        binary_num, similar = retest.similar_binary(trans_df.loc[time_steps-1: len(trans_df)-return_days+i-1, :])
        test_prediction = stock_ml.lstm_predict(model, feature_test_df, time_steps=time_steps)
        binary_test_prediction = 1 if test_prediction >= binary_num else 0
        test_prediction_list.append(binary_test_prediction)

    trans_df.loc[len(trans_df)-len(test_prediction_list):, 'iterated_prediction'] = test_prediction_list
    trans_df.to_csv(f'{stock_code}_iterated_prediction_2.csv')

        
        


    



if __name__== '__main__':
    main()