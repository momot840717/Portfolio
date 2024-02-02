import pandas as pd
import numpy as np
from retest import StockRetest
from datetime import datetime, timedelta
from price_plot import StockMatplot

"""
測試函數跟預測資料區域
訓練好的資料可以在這裡進行回測、繪圖等等，分開出來就不用等機器訓練時間了
"""


df = pd.read_csv('2329_iterated_prediction_2.csv')
retest = StockRetest()
retest_result = retest.strategy_retest(df, 'iterated_prediction')
print(retest_result)