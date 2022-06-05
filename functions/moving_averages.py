import imp
import db_calls 
import pandas as pd
import talib as ta

class Moving_Averages():
    def __init__(self) -> None:
        self.df_tickers = pd.DataFrame()

    def get_tickers(self, letter='A'):
        self.df_tickers = db_calls.select_historical_data_tickers(letter)

    def process_data(self):
        tickers = self.df_tickers
        for ticker in tickers['ticker'].values.tolist():
            df = db_calls.select_historical_data_all(ticker)
            print(ticker)
            _his = pd.DataFrame()
            _his = self._builddata(df)
            _hisBox = _his[_his['sma200'].notna()] #remove any rows where sma200 is a null
            if len(_hisBox) == 0:
                _hisBox = _his[_his['sma50'].notna()]
            if len(_hisBox) == 0:
                _hisBox = _his[_his['ema21'].notna()]
            
            print(_hisBox[['vol50', 'vol_pct', 'ema8', 'ema21', 'sma50', 'sma200', 'id']])   
            self._update_historical_data_moving_avg(_hisBox[['vol50', 'vol_pct', 'ema8', 'ema21', 'sma50', 'sma200', 'id']])
            print("------------------")

    def _update_historical_data_moving_avg(self, df):
        db_calls.update_historical_data_moving_avg(df)

    def _builddata(self, his):
        _his = pd.DataFrame()
        _his["id"] = his['id']
        _his["ema8"] = round(ta.EMA(his['close'], timeperiod = 8),2)
        _his["ema21"] = round(ta.EMA(his['close'], timeperiod = 21),2)
        _his["sma50"] = round(ta.SMA(his['close'], timeperiod=50),2)
        _his["sma200"] = round(ta.SMA(his['close'], timeperiod=200),2)
        vol50 = round(ta.SMA(his['volume'], timeperiod=50),0)
        _his['vol'] = his['volume']
        _his["vol50"] = vol50
        _his['vol_pct'] = round(((his['volume']-vol50)/his['volume']) * 100,0)
        return _his