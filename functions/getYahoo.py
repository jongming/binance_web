import pandas as pd
from pandas_datareader import data as pdr
import sqlite3
import time
import datetime as dt
import sys
import traceback
import pytz 
import datetime

from soupsieve import select
import db_calls
from functions import error_handler as er
from functions import api_calls

historical_data_csv = 'data/historical_data.csv'

class GetYahoo:
    def __init__(self):
        self.df_tickers = pd.DataFrame()
        self.df_yahoo_data = pd.DataFrame()
        # self.error_handler = er.Error_Handler()
        # self.get_IBD_tickers()

    def get_tickers_info(self, isLetter, letter):
        _df = db_calls.select_tickers_last_date(isLetter, letter)
        print("get_tickers_info")
        print(_df)
        self.df_tickers = _df

    def run_singles_gets(self, date_format, ticker, fromDate): #loop through yahoo api one ticker
        _lDate = last_tradingday()
        _fromDate = fromDate
        last_trading_date = _lDate.strftime(date_format)
        _df_holder = pd.DataFrame()
        _df_yahoo = pd.DataFrame()
        _y_list = []
        if len(self.df_tickers) > 0:
            for data in self.df_tickers.values:
                # print(data[1], data[2])
                _ticker = data[0]
                # _y_list = api_calls.get_yahoo_data(_ticker, data[2], last_trading_date)
                _y_list = api_calls.get_yahoo_data(_ticker, _fromDate, last_trading_date)
                if len(_y_list) > 0:
                    _df_yahoo = pd.DataFrame(_y_list)
                    _df_yahoo.insert(0, "ticker", _ticker)
                    # print(_df_yahoo)
                    # print('>>>')
                    frames = [_df_holder, _df_yahoo]
                    _df_holder = pd.concat(frames, axis=0)
                    self.df_yahoo_data = _df_holder
        else:
            _fromDate = _lDate - dt.timedelta(days=210)
            print(f"_fromDate:{_fromDate}   last_trading_date:{last_trading_date}")
            _y_list = api_calls.get_yahoo_data(ticker, _fromDate, last_trading_date)
            if len(_y_list) > 0:
                _df_yahoo = pd.DataFrame(_y_list)
                _df_yahoo.insert(0, "ticker", ticker)
                # print(_df_yahoo)
                # print('>>>')
                frames = [_df_holder, _df_yahoo]
                _df_holder = pd.concat(frames, axis=0)
                self.df_yahoo_data = _df_holder
            

    def run_batch_gets(self, df_data):
        pass

    def save_to_file(self):
        file = 'data/tickers.csv'
        save_df_csv(self.df_tickers, file, False)

    def prepare_data(self, date_format):
        _record_date_db = list(self.df_IBD_tickers.values[0])[1] #get last date on record (IBD_data)
        _record_date_obj = dt.datetime.strptime(_record_date_db, date_format) #change stirng datetime to obj datetime
        _record_date = _record_date_obj + dt.timedelta(days=0) #add one day
        _record_date = _record_date.strftime(date_format)
        _last_trading_date = last_tradingday().strftime(date_format)
        return [_record_date, _last_trading_date]

    def get_data(self, record_date, last_trading_date, group=10):
        _df_yahoo_data = pd.DataFrame()
        _lst_tickers = [data[0] for data in self.df_IBD_tickers.values]
        _lst_tickers_group = [_lst_tickers[i:i + group] for i in range(0, len(_lst_tickers), group)] 
        _sTime = datetime.datetime.now()
        print("***start: " + _sTime.strftime("%m/%d/%Y, %H:%M:%S"))
        for tickers in _lst_tickers_group:
            _pTime = datetime.datetime.now()
            print("***process: " + _pTime.strftime("%m/%d/%Y, %H:%M:%S"))
            df_y = api_calls.get_yahoo_data(tickers, record_date, last_trading_date)
            frames = [_df_yahoo_data, df_y]
            _df_yahoo_data = pd.concat(frames, axis=0)
    
        _eTime = datetime.datetime.now()
        print("***end: " + _eTime.strftime("%m/%d/%Y, %H:%M:%S"))
        print((_eTime - _sTime).total_seconds())
        print("***"*10)
        # print(_df_yahoo_data)
        # print(">"*20)
        self.df_yahoo_data = _df_yahoo_data

    def save_data_from_csv(self):
        _df = read_csv(historical_data_csv)
        self.save_data(_df)
        # print(_df)

    def save_yahoo_data(self):
        self.save_data(self.df_yahoo_data)

    def save_data(self, df):
        # _df = self.df_yahoo_data.stack().reset_index().rename(index=str, columns={"level_1": "Symbols"}).sort_values(['Symbols','Date'])
        _df_data = pd.DataFrame(df.values.tolist(), columns = ["ticker", "date", "high", "low", "open", "close", "volume", "adj_close"])
        _df_data['high'] = round(_df_data['high'],2)
        _df_data['low'] = round(_df_data['low'],2)
        _df_data['open'] = round(_df_data['open'],2)
        _df_data['close'] = round(_df_data['close'],2)
        _df_data['volume'] = round(_df_data['volume'],2)
        _df_data['adj_close'] = round(_df_data['adj_close'],2)
        #Add 2 columns (ticker, date) to the end of df
        _df_data['ticker2'] = _df_data.loc[:, 'ticker']
        _df_data['date2'] = _df_data.loc[:, 'date']
        _df_data['date']= _df_data['date'].astype(str) #convert timestamp to string in dataframe
        _df_data['date2']= _df_data['date2'].astype(str) #convert timestamp to string in dataframe
        # print(">"*20)
        # print(_df_data)
        # print(">"*20)
        db_calls.batch_insert_historical_data(_df_data)
        
    def get_last_saved_data(self):
        return db_calls.select_latest_historical_data()

class GetYahooSingles:
    def __init__(self):
        self.df_IBD_tickers = pd.DataFrame()
        self.df_yahoo_data = pd.DataFrame()

def save_df_csv(df, file, isUpdate=False):
    try:
        if isUpdate:    
            df.to_csv(file, mode='a', header=False, index=False) #update CSV
        else:
            df.to_csv(file, mode='w', index=False) #Save (overwrite) CSV
    except: 
        print("Error while saving")

def read_csv(file):
    df = pd.read_csv(file)
    return df

def last_tradingday():
    lastTradingDay = ''
    nyc_datetime = dt.datetime.now(tz=pytz.timezone('US/Eastern'))
    if nyc_datetime.weekday() == 0: #Monday
        #print('day=0')
        if nyc_datetime.hour < 16:
            #print('hr < 16')
            lastTradingDay = nyc_datetime + dt.timedelta(days=-3)
        if nyc_datetime.hour > 16:
            #print('hr > 16')
            lastTradingDay = nyc_datetime
    elif nyc_datetime.weekday() < 5 and nyc_datetime.weekday() > 0: #Tue to Fri
        #print('day=< 5 and >0')
        if nyc_datetime.hour < 16:
            #print('hr < 16')
            lastTradingDay = nyc_datetime + dt.timedelta(days=-1)
        if nyc_datetime.hour > 16:
            #print('hr > 16')
            lastTradingDay = nyc_datetime 
    elif nyc_datetime.weekday() == 5:
        #print('day=5')
        lastTradingDay = nyc_datetime + dt.timedelta(days=-1)    
    elif nyc_datetime.weekday() ==6:
        #print('day=6')
        lastTradingDay = nyc_datetime + dt.timedelta(days=-2) 
    #return lastTradingDay.strftime('%Y-%m-%d')
    #print('last_tradingday: ' + str(lastTradingDay.date()))
    return lastTradingDay.date() + dt.timedelta(days=1)