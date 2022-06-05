import datetime as dt
import pandas as pd
import sqlite3, traceback, sys

database = "data/InvestorDB.db"

def select_historical_data(ticker, days=30):
    numDays = dt.date.today() - dt.timedelta(days)
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        # print(f"select_historical_data - Successfully Connected to SQLite - ticker:{ticker}")
        
        query = sqliteConnection.execute("SELECT on_date as 'date', high, low, open, adj_close, LAG(adj_close, 1, 0) OVER (ORDER BY on_date ASC) pre_close, volume, ticker as 'tk' FROM historical_data WHERE ticker = ? AND on_date > ? order by on_date ASC;",[ticker, numDays])

        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        print(f"Failed: select_historical_data - ticker:{ticker}")
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)
        print('Printing detailed SQLite exception traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        pass

    if (sqliteConnection):
        sqliteConnection.close()
        # print("select_historical_data - The SQLite connection is closed")  

def select_all_tickers_historical_data():
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        # print("select_all_tickers_historical_data - Successfully Connected to SQLite")

        query = sqliteConnection.execute("SELECT DISTINCT(ticker) as ticker FROM historical_data ORDER BY ticker;")
        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        print("Failed to select_all_tickers_historical_data")
        print("Exception class is: ", error.__class__)
        print("Exception is", error.args)
        print('Printing detailed SQLite exception traceback: ')
        exc_type, exc_value, exc_tb = sys.exc_info()
        print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        pass

    if (sqliteConnection):
        sqliteConnection.close()
        # print("select_all_tickers_historical_data - The SQLite connection is closed")  

def is_consolidating(df, lookback=15, percent = 2):
    recent_candlesticks = df[lookback*-1:]
    max_close = recent_candlesticks['adj_close'].max()
    min_close = recent_candlesticks['adj_close'].min()
    threshold = 1 - (percent / 100)
    if min_close > (max_close * threshold):
        return True   
    return False
    
def is_breaking_out(df, lookback=15, percent = 2):
    last_close = df[-1:]['adj_close'].values
    
    #is stock consolidating up to but not including the most recent close 
    if is_consolidating(df[:-1], percent=percent):
        #get records not including most recent close
        recent_closes = df[(lookback+1)*-1:-1]
        if last_close > recent_closes['adj_close'].max():
            return True
    return False


df_all = select_all_tickers_historical_data()

for ticker in df_all.ticker:
    _df = select_historical_data(ticker)
    if is_consolidating(_df, lookback = 10, percent=2):
        print("{} is consolidating".format(ticker))
    
    if is_breaking_out(_df, lookback = 10, percent=2):
        print("{} is breaking out".format(ticker))

    

    
