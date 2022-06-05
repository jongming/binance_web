import sqlite3
# import traceback
import sys
import datetime as dt
from unittest import result
# from numpy import rec
import pandas as pd
from functions import error_handler
# import re

def _cleanString(str):
    # return re.sub('\w+','', str)
    # return re.sub('\W+','', str )
    return str

database = "data/InvestorDB.db"

def batch_insert_Finviz(df):
    sql = "INSERT INTO Finviz (ticker, name, sector, industry, country) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT ticker FROM Finviz WHERE ticker = ?)"
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        cursor = sqliteConnection.cursor()
        cursor.executemany(sql, df.values.tolist())
        sqliteConnection.commit()
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: batch_insert_Finviz")

    finally:
        if (sqliteConnection):
            cursor.close()
            sqliteConnection.close() 


def batch_insert_Finviz_r_perform(df):
    # sql = "INSERT INTO Finviz_r_perform (on_date, industry, perfT, perfW, perfM) VALUES (?,?,?,?,?)"
    sql = "INSERT INTO Finviz_r_perform (on_date, industry, perfT, perfW, perfM) SELECT ?,?,?,?,? WHERE NOT EXISTS (SELECT * FROM Finviz_r_perform WHERE industry = ? AND on_date = ?)"
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        cursor = sqliteConnection.cursor()
        cursor.executemany(sql, df.values.tolist())
        sqliteConnection.commit()
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: batch_insert_Finviz_r_perform")

    finally:
        if (sqliteConnection):
            cursor.close()
            sqliteConnection.close() 

def batch_insert_historical_data(df_all):
    yahoo_sql = "INSERT INTO historical_data (ticker, on_date, high, low, open, close, volume, adj_close) SELECT ?,?,?,?,?,?,?,? WHERE NOT EXISTS (SELECT * FROM historical_data WHERE ticker=? AND on_date=?)"
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        cursor = sqliteConnection.cursor()
        cursor.executemany(yahoo_sql, df_all.values.tolist())
        sqliteConnection.commit()
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: batch_insert_historical_data")

        # print("Failed: batch_insert_historical_data")
        # print("Exception class is: ", error.__class__)
        # print("Exception is", error.args)
        # print('Printing detailed SQLite exception traceback: ')
        # exc_type, exc_value, exc_tb = sys.exc_info()
        # print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if (sqliteConnection):
            cursor.close()
            sqliteConnection.close() 

def if_IBD_daily_exist(date):
    try:
        conn = sqlite3.connect(database)
        cur = conn.cursor()
        cur.execute("SELECT * FROM IBD_Data WHERE on_date=? LIMIT 1", (date,))

        rows = cur.fetchall()
        cur.close()
        conn.close()

        return len(rows) > 0
    
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: if_IBD_daily_exist")

def save_IBD_daily(numDate, rs_data, stocks_data):
    
    sqliteConnection = sqlite3.connect(database, timeout=10)
    cursor = sqliteConnection.cursor()

    try:
        _sql = "INSERT INTO IBD_Data (ticker, cmp, eps, rs, smr, accdis, fiftytwowk, price, price_change, vol_percent, volume, pe, on_date) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
        cursor.executemany(_sql, rs_data.values.tolist())
        sqliteConnection.commit()


    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: save_IBD_daily: rs_data")

    try:
        _sql = "INSERT INTO stock (ticker, name, industry, date_added) SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT * FROM stock WHERE ticker = ?)"
        cursor.executemany(_sql, stocks_data.values.tolist())
        sqliteConnection.commit()
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: save_IBD_daily: stocks_data")
    finally:
        if (sqliteConnection):
            cursor.close()
            sqliteConnection.close()    

def select_alerts():
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite - select_alerts")

        cursor.execute("SELECT a.ticker, a.price, a.open_date, IFNULL(a.triggered_date, '') as 'triggered_date', " +
            "(SELECT ROUND(h.close,2) as close FROM historical_data h WHERE h.ticker = a.ticker ORDER BY h.on_date DESC LIMIT 1) as 'close' " + 
            "FROM alerts a ORDER BY a.ticker, a.open_date DESC;")
        records = cursor.fetchall()
        cursor.close()

        column_names = [ "ticker", "price", "open_date", "triggered_date", "close"]
        df = pd.DataFrame(records, columns = column_names)
        return df
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: select_alerts")

        # print("Failed: select_alerts")
        # print("Exception class is: ", error.__class__)
        # print("Exception is", error.args)
        # print('Printing detailed SQLite exception traceback: ')
        # exc_type, exc_value, exc_tb = sys.exc_info()
        # print(traceback.format_exception(exc_type, exc_value, exc_tb))
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("SQLite connection closed - select_alerts")  

def select_Finviz_Performance(sort_by):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite - select_Finviz_Performance")
        if sort_by == "weekly":
            cursor.execute("SELECT industry from Finviz_r_perform WHERE on_date = (SELECT MAX(on_date) FROM Finviz_r_perform) ORDER by perfW DESC;")
        elif sort_by == "monthly":
            cursor.execute("SELECT industry from Finviz_r_perform WHERE on_date = (SELECT MAX(on_date) FROM Finviz_r_perform) ORDER by perfM DESC;")
        else:
            # cursor.execute("SELECT on_date, industry, perfT FROM Finviz_r_perform order by on_date, perfT;")
            cursor.execute("SELECT industry from Finviz_r_perform WHERE on_date = (SELECT MAX(on_date) FROM Finviz_r_perform) ORDER by perfT DESC limit 5;")
        records = cursor.fetchall()

        cursor.close()

        return records
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: select_Finviz_Performance:" + sort_by)
    finally:
        if sqliteConnection:
            sqliteConnection.close() 

def select_Finviz_Performance_industry(industry):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT on_date, industry, perfT, perfW, perfM FROM Finviz_r_perform WHERE industry = ?" +
            "ORDER BY on_date ;", (industry,))
        records = cursor.fetchall()
        cursor.close()

        column_names = ["on_date", "industry", "perfT", "perfW", "perfM"]
        df = pd.DataFrame(records, columns = column_names)
        return df
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: select_Finviz_Performance_data")
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def select_Finviz_Performance_data():
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()

        cursor.execute("SELECT on_date, industry, perfT, perfW, perfM FROM Finviz_r_perform WHERE on_date = " +
            "(SELECT max(on_date) FROM Finviz_r_perform) ORDER BY perfT DESC, perfW DESC, perfM DESC;")
        records = cursor.fetchall()
        cursor.close()

        column_names = ["on_date", "industry", "perfT", "perfW", "perfM"]
        df = pd.DataFrame(records, columns = column_names)
        return df
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: select_Finviz_Performance_data")
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def select_tickers_last_date(letter):
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        query = sqliteConnection.execute("SELECT t.ticker_IBD, t.ticker_yahoo, max(on_date) as date FROM historical_data h " +
                            "INNER JOIN ticker_lookup t ON t.ticker_IBD=h.ticker " +
                            "WHERE ticker like ? " +
                            "group by ticker ORDER BY ticker;", (letter+'%',))
        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed to select_tickers_last_date: " + letter)

    finally:
        if (sqliteConnection):
            sqliteConnection.close()
 

def select_IBD_tickers_by_rs(cmp=80, rs=80):
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        cursor = sqliteConnection.cursor()
        cursor.execute("select ticker from IBD_Data where cmp > ? AND rs > ? AND " 
        "on_date = (SELECT max(on_date) FROM IBD_Data) ORDER by ticker;", (cmp, rs,))
        # records = cursor.fetchall()
        cols = [column[0] for column in cursor.description]
        results= pd.DataFrame.from_records(data = cursor.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed to select_IBD_tickers_by_rs")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def select_IBD_tickers_byVariables(cmp=80, rs=80, price_change=0, vol_percent=50, volume=400000):
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        cursor = sqliteConnection.cursor()
        #cursor.execute("select ticker, cmp, eps, rs, smr, accdis, fiftytwowk, price, price_change, vol_percent, volume, pe " + 
        cursor.execute("select ticker from IBD_Data where cmp > ? AND rs > ? AND price_change > ? AND vol_percent > ? AND volume > ? AND " +
            "on_date = (SELECT MAX(on_date) FROM IBD_Data) ORDER by cmp DESC limit 10;", (cmp, rs, price_change, vol_percent, volume))
        records = cursor.fetchall()
        cursor.close()
        return records
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed to select_IBD_tickers_by_rs")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def select_IBD_data(ticker):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute("select d.on_date as date, d.cmp, d.eps, d.rs, replace(d.smr,'..',0) as SMR, g1.value as SMR_value, d.accdis as accdis, g2.value as accdis_value, s.industry as iindustry, f.sector, f.industry as findustry from IBD_Data d INNER JOIN stock s ON d.ticker = s.ticker INNER JOIN Finviz f ON f.ticker = d.ticker LEFT JOIN grading_values g1 ON g1.letter = d.SMR LEFT JOIN grading_values g2 ON g2.letter = d.accdis where d.ticker = ?  ORDER BY d.on_date;", (ticker,))
        records = cursor.fetchall()
        cursor.close()

        column_names = [ "date", "CMP", "EPS", "RS", "SMR", "SMR_value", "AD", "accdis_value", "iindustry", "sector", "findustry"]
        df = pd.DataFrame(records, columns = column_names)
        return df
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: select_IBD_data")
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def select_IBD_data_byDate(date):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute("select on_date, ticker, cmp, eps, rs, smr, accdis from IBD_Data  where on_date = ?;", (date,))
        records = cursor.fetchall()
        cursor.close()

        column_names = ["on_date", "ticker", "cmp", "eps", "rs", "SMR", "accdis"]
        df = pd.DataFrame(records, columns = column_names)
        return df
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: select_IBD_data_byDate " + date)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def select_IBD_tickers_notin_Finviz():
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        query = sqliteConnection.execute("SELECT DISTINCT(ticker) from IBD_Data where ticker not in (select ticker from Finviz) ORDER BY ticker;")
        cols = ['ticker']
        _df = pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return _df
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed to select_IBD_tickers_notin_Finviz")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()


def xget_IBD_RSData(ticker):
    data = select_IBD_data(ticker)
    column_names = [ "date", "CMP", "EPS", "RS", "SMR", "SMR_value", "AD", "accdis_value", "iindustry", "sector", "findustry"]
    df = pd.DataFrame(data, columns = column_names)
    # display_df = df[["date", "CMP", "EPS", "RS", "SMR", "SMR_value", "AD", "accdis_value", "iindustry", "sector", "findustry"]]
    
    return df

def select_latest_historical_data():
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        query = sqliteConnection.execute("select ticker, on_date, round(high,2) high, round(low,2) low, round(open,2) open, round(close,2) close," +
            "round(volume,2) volume, round(adj_close,2) adj_close " +   
            "from historical_data where on_date = (select max(on_date) from historical_data) order by ticker;")

        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed: select_latest_historical_data")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def select_historical_data(ticker, days=30):
    numDays = dt.date.today() - dt.timedelta(days)
    ticker = _cleanString(ticker)
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        query = sqliteConnection.execute("SELECT on_date as 'date', high, low, open, adj_close, LAG(adj_close, 1, 0) OVER (ORDER BY on_date ASC) pre_close, volume, ticker as 'tk' FROM historical_data WHERE ticker = ? AND on_date > ? order by on_date ASC;",[ticker, numDays])

        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed: select_historical_data - ticker:{ticker}")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def select_historical_data_all(ticker):
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        query = sqliteConnection.execute("SELECT * FROM historical_data WHERE ticker = ? order by on_date ASC;",[ticker])

        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed: select_historical_data_all: {ticker}")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def select_historical_industry_performance(industry):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT date1 as on_date, sector, industry, SUM(close) as close, " +
            "SUM(LastDClose) as prevd_close, ROUND((SUM(close) - SUM(LastDClose)) / SUM(close) * 100,2) as daily_diff, " +
            "SUM(LastWClose) as prevw_close, ROUND((SUM(close) - SUM(LastWClose)) / SUM(close) * 100,2) as weekly_diff " +
            "FROM ( " +
            "SELECT f.sector as  sector, f.industry as industry, h.on_date as date1, ROUND(h.close,2) as close, " +
            "ROUND(LAG(h.close, 1, 0) OVER (PARTITION BY h.ticker ORDER BY h.on_date),2) as LastDClose, " +
            "ROUND(LAG(h.close, 5, 0) OVER (PARTITION BY h.ticker ORDER BY h.on_date),2) as LastWClose " +
            "FROM historical_data h INNER JOIN Finviz f ON f.ticker = h.ticker " +
            "WHERE f.industry = ? ORDER BY h.on_date desc) " +
            "GROUP BY date1 ORDER BY date1;", (industry,))
        records = cursor.fetchall()
        cursor.close()

        column_names = ["on_date", "sector", "industry", "daily_close", "prev_close", "daily_diff", "prevw_close", "weekly_diff"]
        df = pd.DataFrame(records, columns = column_names)
        return df
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(">>> Failed: select_Finviz_Performance_data")
    finally:
        if sqliteConnection:
            sqliteConnection.close()

def select_historical_data_tickers(letter):
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        query = sqliteConnection.execute("SELECT ticker FROM historical_data WHERE ticker like ? AND " +
            "on_date = (SELECT max(on_date) from historical_data)GROUP BY ticker;", (letter+'%',))
        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed to select_historical_data_tickers: " + letter)
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def select_all_tickers():
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        query = sqliteConnection.execute("SELECT DISTINCT(ticker) as ticker FROM historical_data " +
                                        # " WHERE ticker like 'M%' or ticker like 'N%' "+
                                        #" WHERE ticker like 'M%' "+
                                        " ORDER BY ticker;")
        cols = [column[0] for column in query.description]
        results= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        return results
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed to select_all_tickers_historical_data")
    finally:
        if (sqliteConnection):
            sqliteConnection.close()

def select_ticker_and_industry():
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT f.ticker, industry, i.cmp, i.eps, i.rs, i.smr, i.accdis " +
            "FROM Finviz f INNER JOIN IBD_Data i ON i.ticker=f.ticker " +
            "WHERE i.on_date = (SELECT max(on_date) FROM IBD_Data) " +
            "ORDER BY industry, i.rs DESC, i.cmp DESC;")
        records = cursor.fetchall()
        cursor.close()
        
        cols = ['ticker', 'industry', 'CMP', 'EPS', 'RS', 'SMR', 'AD']
        df= pd.DataFrame.from_records(records, columns = cols)
        return df
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed: select_ticker_and_industry")
    finally:
        if sqliteConnection:
            sqliteConnection.close() 

def select_ticker_by_industry(industry):
    try:
        sqliteConnection = sqlite3.connect(database)
        cursor = sqliteConnection.cursor()
        query = sqliteConnection.execute("SELECT i.ticker from IBD_Data i INNER JOIN Finviz f ON i.ticker = f.ticker WHERE i.on_date = " +
            "(SELECT max(on_date) FROM IBD_Data) AND f.industry = ? " +
            "ORDER BY i.rs DESC, i.cmp DESC;", (industry,))
        
        cols = [column[0] for column in query.description]
        df= pd.DataFrame.from_records(data = query.fetchall(), columns = cols)
        tickers = df['ticker'].tolist()
        return tickers
        
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed: select_ticker_by_industry")
    finally:
        if sqliteConnection:
            sqliteConnection.close()       


def update_historical_data_moving_avg(df):
    sql = "UPDATE historical_data SET vol50=?, vol_pct=?, ema8=?, ema21=?, sma50=?, sma200=? WHERE id=?"
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        cursor = sqliteConnection.cursor()
        cursor.executemany(sql, df.values.tolist())
        sqliteConnection.commit()
    except sqlite3.Error as error:
        _error = error_handler.Error_Handler(error, sys.exc_info())
        _error.save_to_errorlog(f">>> Failed: update_historical_data_moving_avg")
    finally:
        if sqliteConnection:
            sqliteConnection.close()  