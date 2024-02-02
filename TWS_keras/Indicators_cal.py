import talib
import numpy as np
import copy
import pandas as pd


"""
如果安裝TA-lib 失敗 利用pip debug --verbose的改檔名再安裝方法
https://zhuanlan.zhihu.com/p/345127194

如果使用 python 3.11
talib檔案安裝包: https://forum.klang.org.cn/assets/uploads/ta_lib-0.4.25-cp311-cp311-win_amd64.whl
來源: https://www.jianshu.com/p/f60adb869364

"""

class Indicators:
    def __init__(self) -> None:
        pass


    def cal_rsi(self, close_series: pd.Series, period: int=6) -> pd.Series:
        """ RSI 預設週期6, 需要12 就新增參數 period=12

        Args:
            close_series (pd.Series): 收盤價
            period (int, optional): 計算週期. Defaults to 6.

        Returns:
            pd.Series: rsi計算結果
        """
        cal_series = copy.deepcopy(close_series)
        rsi_series = np.round(talib.RSI(cal_series, timeperiod=period), 3)
        return rsi_series
    

    def cal_macd(self, close_series: pd.Series, fastperiod=12, slowperiod=26, signalperiod=9) -> tuple[pd.Series]:
        """ 計算 macd柱 快、慢線 將返回三個數值
            注意台股的 MACD 的數值名稱順序是 DIF, MACD, OSC

        Args:
            close_series (pd.Series): _description_
            fastperiod (int, optional): . Defaults to 12.
            slowperiod (int, optional): . Defaults to 26.
            signalperiod (int, optional): . Defaults to 9.

        Returns:
            pd.Series: DIF MACD OSC(台股)
        """
        cal_series = copy.deepcopy(close_series)
        # 使用台股MACD順序
        return np.round(talib.MACD(cal_series, fastperiod, slowperiod, signalperiod), 4)
    

    def cal_kdj(self, close_series, high_series, low_series, fast_period=9, slow_period=3, matype=1)-> tuple[pd.Series]:
        """ KDJ 參數使用技巧 參考: https://xueqiu.com/1747761477/198676825

        Args:
            close_series (pd.Series): 收盤
            high_series (pd.Series): 最高
            low_series (pd.Series): 最低
            fast_period (int, optional): . Defaults to 9.
            slow_period (int, optional): . Defaults to 3.
            matype (int, optional): . Defaults to 1.

        Returns:
            tuple[pd.Series]: (K, D, J)
        """
        
        slowk, slowd = np.round(talib.STOCH( high_series, low_series, close_series, 
                                    fastk_period=fast_period,
                                    slowk_period=2*slow_period-1, 
                                    slowk_matype=matype, 
                                    slowd_period=2*slow_period-1, 
                                    slowd_matype=matype
                                ), 3)
        
        return slowk, slowd, 3 * slowk - 2 * slowd
        

    def cal_ma(self, close_series, period):
        return talib.SMA(close_series, timeperiod=period)
        