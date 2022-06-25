import db_calls
import pandas as pd

class Consolidate:
    def __init__(self) -> None:
        pass

    def get_isConsolidate_isBreak(self, cmp=80, rs=80, lookback=10, pcent=3):
        _breakout_list =[]
        _stocklist = []
        # df_all = db_calls.select_all_tickers()
        df_all = db_calls.select_IBD_tickers_by_rs(cmp, rs)
        # print(".................")
        # print(df_all)
        for ind in df_all.index:
            ticker = df_all['ticker'][ind]
            _result = {}
            _df = db_calls.select_historical_data(ticker, days=30)
            _is_consolidating = self.is_consolidating(_df, lookback = lookback, pcent=pcent)
            _is_breaking_out = self.is_breaking_out(_df, lookback = lookback, pcent=pcent)
            if _is_consolidating:
                _result['ticker'] = ticker
                _result['is_cons'] = _is_consolidating
                _result['is_break'] = _is_breaking_out
                _breakout_list.append(_result)
                _stocklist.append(ticker)
        # print(">>>>>>>>>>>>>")
        # print(_breakout_list)
        # print(_stocklist)
        return [_stocklist, _breakout_list]

    def is_consolidating(self, df, lookback=15, pcent = 2):
        lookback = int(lookback)
        pcent = int(pcent)
        # print("lookback:" + str(lookback) + " percent:" +str(pcent))
        # print(df)
        # print(df[-10:])
        # _lookback = lookback * -1
        # _lookback = -10
        # print("lookback:" + str(_lookback))
        _recent_candlesticks = df[lookback:]
        # print("~~~~~~~~~~~~~~~~~~~~~~")
        # print(_recent_candlesticks)
        # print(_recent_candlesticks['adj_close'].max())
        # print(_recent_candlesticks['adj_close'].min())
        _max_close = _recent_candlesticks['adj_close'].max()
        _min_close = _recent_candlesticks['adj_close'].min()
        # print("max:" + str(_max_close) + " min:" + str(_min_close))
        # print("++++++++++++++++=")
        # print("pcent type: " + str(type(pcent)))
        threshold = 1 - (pcent / 100)
        if _min_close > (_max_close * threshold):
            return True   
        return False

    def is_breaking_out(self, df, lookback=15, pcent = 2):
            lookback = int(lookback)
            pcent = int(pcent)
            _last_close = df[-1:]['adj_close'].values
            #is stock consolidating up to but not including the most recent close 
            if self.is_consolidating(df[:-1], lookback=lookback, pcent=pcent):
                #get records not including most recent close
                recent_closes = df[(lookback+1)*-1:-1]
                if _last_close > recent_closes['adj_close'].max():
                    return True
            return False
    