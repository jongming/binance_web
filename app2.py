# save this as app.py
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from alpha_vantage.timeseries import TimeSeries
from flask_cors import CORS
import time
import datetime as dt
import sqlite3
import traceback
import sys
import pandas as pd

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = '527f6d739a5e44c9b502cc6136545c217454e7f4de57f6f1'
app.secret_key = b'527f6d739a5e44c9b502cc6136545c217454e7f4de57f6f1'
database = "data/InvestorDB.db"

def select_historical_data(ticker):
    date60 = dt.date.today() - dt.timedelta(days=180)
    try:
        sqliteConnection = sqlite3.connect(database, timeout=10)
        print(f"select_historical_data - Successfully Connected to SQLite - ticker:{ticker}")
        
        query = sqliteConnection.execute("SELECT on_date as 'date', high, low, open, adj_close, LAG(adj_close, 1, 0) OVER (ORDER BY on_date ASC) pre_close, volume, ticker as 'tk' FROM historical_data WHERE ticker = ? AND on_date > ? order by on_date ASC;",[ticker, date60])

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
        print("select_historical_data - The SQLite connection is closed")   

@app.route("/")
def index():
    print('Index')
    title = "Coinview"
    return render_template('index.html', title = title)

@app.route('/buy', methods=['POST'])
def buy():
    print('Buy')
    print(request.form)
    return 'buy'

@app.route('/sell')
def sell():
    print('Sell')
    return 'sell'

@app.route('/settings')
def settings():
    print('Settings')
    return 'settings'

@app.route('/history')
def history():
    print("history")
 
    df = pd.DataFrame()
    def appendDF(_df1, _df2):
        _df = pd.DataFrame()
        _df = pd.concat([_df1, _df2], axis=0)
        return _df

    def process_data(df, ticker):
        processed_data = {}
        processed_candlesticks = []
        processed_volumes = []
        for _data in df[df['tk']==ticker].values:
            _candlestick = { 
                "time": _data[0], 
                "open": _data[3],
                "high": _data[1], 
                "low": _data[2], 
                "close": _data[4]
            }
            processed_candlesticks.append(_candlestick)

            if _data[5] < _data[4]:
                _color = 'rgba(0, 150, 136, 0.8)'
            else:
                _color = "rgba(255,82,82, 0.8)"
            _volume = {
                "time": _data[0], 
                "value": _data[6],
                "color": _color
            }
            processed_volumes.append(_volume)
        
        processed_data['ticker'] = ticker
        processed_data['candlesticks'] = processed_candlesticks
        processed_data['volume'] = processed_volumes
        return processed_data   

    stocks = ('AAPL', 'TSLA', 'MSFT')
    for stock in stocks:
        _df = select_historical_data(stock)
        df = appendDF(df, _df)

    master_data = {}
    print(df)
    print("*******************")

    stocks_list = ['stock1', 'stock2', 'stock3', 'stock4', 'stock5', 'stock6', 'stock7', 'stock8', 'stock9', 'stock10']
    s_list_count = 0
    for stock in stocks:
        master_data[stocks_list[s_list_count]] = process_data(df, stock)
        s_list_count += 1

    return jsonify(master_data)

    
    
