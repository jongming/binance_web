import db_calls
import pandas as pd

class CrossingMA():
    def __init__(self) -> None:
        pass

    def get21Crossing50(self, lookback):
        tickers = db_calls.select_historical_data_21_cross_50(lookback)
        ticker_list = [i for sub in tickers for i in sub]
        return ticker_list

    def get8Crossing21(self, lookback):
        tickers = db_calls.select_historical_data_8_cross_21(lookback)
        ticker_list = [i for sub in tickers for i in sub]
        return ticker_list    