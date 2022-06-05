from pandas_datareader import data as pdr
import traceback, sys
import pandas as pd
from sympy import im
from functions import error_handler


def get_yahoo_data(ticker, start_date, end_date):
    print(f'get_yahoo_data: {ticker} {start_date} {end_date}') 
    df_yahoo_data = pd.DataFrame()
    try:
        df_yahoo_data = pdr.get_data_yahoo(ticker, start_date, end_date)
    except Exception as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.error_from_yahoo_import(ticker)
        # _exc_type, _exc_value, _exc_tb = sys.exc_info()
        # _traceback = traceback.format_exception(_exc_type, _exc_value, _exc_tb)
        # _exception_text = "Exception class: " + error.__class__ + "\n Exception: " + error.args + "\n Traceback: " + _traceback
        _error.save_to_errorlog(">>> Failed to get data from yahoo for ticker: " + ticker)
    finally:
        if len(df_yahoo_data) > 0:    
            df_yahoo_data = df_yahoo_data.reset_index().values.tolist() #reset index so date is part of the values
        return df_yahoo_data 