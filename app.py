# save this as app.py
# from crypt import methods
# from doctest import master
# from lib2to3.pgen2.pgen import DFAState
from flask import Flask, render_template, request, url_for, flash, redirect, jsonify
from flask_cors import CORS
import time
import datetime as dt
from numpy import sort
import pandas as pd
import json
from urllib.parse import urlparse, unquote
import os
import db_calls
from functions import api_calls
# import functions.globalCharts as gcharts
from functions import getYahoo as gyahoo
from functions import globalCharts as gcharts
from functions import getIBD as gIBD
from functions import getFinviz as gFinviz
from functions import moving_averages as ma

app = Flask(__name__)
CORS(app)
app.debug = True

date_format = '%Y-%m-%d'

def appendDF(_df1, _df2): #append two dataFrames into one dataFrames
    # _df = pd.DataFrame()
    # _df = pd.concat([_df1, _df2], axis=0)
    # return _df
    pass
 
def process_data(df, ticker): #build data structure for Tradingview chart
        # processed_data = {}
        # processed_candlesticks = []
        # processed_volumes = []
        # for _data in df[df['tk']==ticker].values:
        #     _candlestick = { 
        #         "time": _data[0], 
        #         "open": _data[3],
        #         "high": _data[1], 
        #         "low": _data[2], 
        #         "close": _data[4]
        #     }
        #     processed_candlesticks.append(_candlestick)

        #     if _data[5] < _data[4]:
        #         _color = 'rgba(0, 150, 136, 0.8)'
        #     else:
        #         _color = "rgba(255,82,82, 0.8)"
        #     _volume = {
        #         "time": _data[0], 
        #         "value": _data[6],
        #         "color": _color
        #     }
        #     processed_volumes.append(_volume)
        
        # processed_data['ticker'] = ticker
        # processed_data['candlesticks'] = processed_candlesticks
        # processed_data['volume'] = processed_volumes
        # return processed_data  
        pass

@app.route("/")
def index():
    print('Index')
    title = "Coinview"
    return render_template('index.html', title = title)

@app.route('/getdata', methods=['GET', 'POST'])
def getdata():
    print("Get Data")
    result = False
    df_data = ""
    get_external_data = ""
    #If page if reloaded via form submit
    if request.method == "POST":
        result = "Wait"
        get_external_data = request.form['get_external_data']
        # print("get_external_data: " + get_external_data)
        # print("---"* 10)

    if get_external_data == "finviz_daily":
        print("finviz_daily")
        _getFinviz = gFinviz.GetFinviz()
        _getFinviz.scrape_daily_data()
        _df = _getFinviz.get_data()
        df_data = _df.values.tolist()
        result = True
        
    if get_external_data == "ibd_daily":
        print("ibd_daily")
        _select_date = request.form['ibd_date']
        _getIBD = gIBD.GetIBD()
        _getIBD.scrape_IBD_data(_select_date)
        _getIBD.save_IBD_data(_select_date)
        _df = _getIBD.get_IBD_data(_select_date)
        df_data = _df.values.tolist()
        result = True

    if get_external_data == "Save Tickers to CSV":
        getYahooData = gyahoo.GetYahoo()
        getYahooData.get_tickers_info()
        # getYahooData.run_singles_gets(date_format)
        print("df_yahoo_data")
        print(getYahooData.df_tickers)
        getYahooData.save_to_file()
        
    if get_external_data == "Save Yahoo daily":
        getYahooData = gyahoo.GetYahoo()

        #save data from running yahoo get
        for letter in list(map(chr,range(ord('a'),ord('z')+1))):
            getYahooData.get_tickers_info(letter)
            getYahooData.run_singles_gets(date_format)
            print(getYahooData.df_yahoo_data)
            getYahooData.save_yahoo_data()


        #get data from csv and save to db
        # getYahooData.save_data_from_csv() 


        _df = getYahooData.get_last_saved_data() #for displaying last saved data
        df_data = _df.values.tolist()
        result = True

    if get_external_data == "Get Finviz ticker info":
        print("Get Finviz ticker info")
        _getFinviz = gFinviz.GetFinviz()
        _df_tickers = pd.DataFrame()
        _df_tickers = _getFinviz.tickers_notin_Finviz()
        # print(_df_tickers)
        _df_scrape_stock_info = _getFinviz.scrape_stock_info(_df_tickers)
        # print(_df_scrape_stock_info)
        _getFinviz.save_Finviz(_df_scrape_stock_info)
        df_data = _df_scrape_stock_info.values.tolist()
        result = True

    if get_external_data == "Moving Average":
        print("Moving Average")
        moving_average = ma.Moving_Averages()
        moving_average.get_tickers("M")
        moving_average.process_data()

    master_data = {"getdata": {"action": result}}
    jdata = df_data

    return render_template('getdata.html',
        jmaster_data = json.dumps(master_data),
        jdata = json.dumps(jdata)
        # jdata = jdata
    )

@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    print("scanner")
    master_data = []
    master_rsdata = []
    _breakout_list = [] 
    action_data = []
    scan_data = ""

    dict = request.form
    for key in dict:
        print(key + " " + dict[key])

    print("*******************")
    if request.method == "POST":
        scan_data = request.form['scan_data']
  
    if scan_data == "Get Volume Profile":
        print(">>>>>>>>>Get Volume Profile")
        form_cmp = request.form['cmp']
        form_rs = request.form['rs']
        form_price_change = request.form['price_change']
        form_vol_percent = request.form['vol_percent']
        form_vol = request.form['vol']
        _gcharts = gcharts.GlobalCharts()
        lst_tickers = _gcharts.getVolumeChange(form_cmp, form_rs, form_price_change, form_vol_percent, form_vol)
        # print(list(lst_tickers))
        _df = _gcharts.getHistoricalData(list(lst_tickers))
        # print(_df)
        _consolidate_list = list(_df['tk'].unique())
        # print("]]]]]]]]]]]]]]]]]]]]")
        # print(_consolidate_list)
        _gcharts.build_list(_consolidate_list)
        master_data = _gcharts.build_master_data(_consolidate_list)
        # print("------------master_date-----------")
        # print(master_data)
        master_rsdata = _gcharts.build_master_rsdata(_consolidate_list)
        action_data = {"getdata": "consolidate"}

    if scan_data == "consolidate":
        form_cmp = request.form['cmp']
        form_rs = request.form['rs']
        form_lookback = request.form['lookback']
        form_percent = request.form['percent']
        _file = 'data/ticker_rs_data.csv'
        _consolidate_list =[]

        _gcharts = gcharts.GlobalCharts()
        _lists = _gcharts.get_isConsolidate_isBreak(cmp=form_cmp, rs=form_rs, lookback=form_lookback, pcent=form_percent)
        # print("_list")
        # print(_lists)
        _consolidate_list = _lists[0]
        _breakout_list = _lists[1]
        _df = _gcharts.getHistoricalData(_consolidate_list)
        # _columns = ['date', 'high', 'low', 'open', 'adj_close', 'pre_close', 'volume', 'tk']
        # _df = _gcharts.getHistoricalData_fromcsv(_file, _columns)
        _consolidate_list = list(_df['tk'].unique())
        print("]]]]]]]]]]]]]]]]]]]]")
        print(_consolidate_list)
        _gcharts.build_list(_consolidate_list)
        master_data = _gcharts.build_master_data(_consolidate_list)
        print("------------master_date-----------")
        print(master_data)
        master_rsdata = _gcharts.build_master_rsdata(_consolidate_list)
        action_data = {"getdata": "consolidate"}

    return render_template('scanner.html',
        jaction_data = json.dumps(action_data),
        jstocks_data = json.dumps(master_data),
        jrs_data = json.dumps(master_rsdata),
        jstock_list = json.dumps(_breakout_list)
        )

@app.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    df_alerts = pd.DataFrame()
    df_alerts = db_calls.select_alerts()
    # print(df_alerts)

    def process_alert_data(ticker, df):
        # _processed_data = {}
        # _ticker = []
        # _price = []
        # _open_date = []
        # _triggered_date = []
        # _close = []
        # for _record in df.values:
        #     _ticker.append(ticker)
        #     _price.append(_record[1])
        #     _open_date.append(_record[2])
        #     _triggered_date.append(_record[3])
        #     _close.append(_record[4])
        # _processed_data['ticker'] = _ticker
        # _processed_data['price'] = _price
        # _processed_data['open_date'] = _open_date
        # _processed_data['triggered_date'] = _triggered_date
        # _processed_data['close'] = _close
        # return _processed_data
        pass

    stocklist = list(df_alerts.ticker.unique())
    df_stocks = pd.DataFrame()
    for stock in stocklist:
        _df_stocks = db_calls.select_historical_data(stock, days=180)
        df_stocks = appendDF(df_stocks, _df_stocks)

    # print(df_stocks)

    #build stock_list dynamically based on number of tickers. stock_list = ['','',''] 
    ticker_list = []
    for x in range(len(df_alerts.index)):
        _listItem = 'ticker'+str(x+1)
        ticker_list.append(_listItem)

    alert_data = {}
    _count = 0
    for ticker in list(df_alerts.ticker.unique()):
        _df = df_alerts[df_alerts.ticker == ticker]
        alert_data[ticker_list[_count]] = process_alert_data(ticker, _df)
        _count+=1

    #build stock_list dynamically based on number of tickers. stock_list = ['','',''] 
    stocks_list = []
    for x in range(len(stocklist)):
        _listItem = 'stock'+str(x+1)
        stocks_list.append(_listItem)

    s_list_count = 0
    master_data = {}
    master_rsdata = {}
    #build and merge all data structure into master_rsdata
    for stock in stocklist:
        master_data[stocks_list[s_list_count]] = process_data(df_stocks, stock)
        # _df_RS = db_calls.get_IBD_RSData(stock)
        # master_rsdata[stocks_list[s_list_count]] = process_rsdata(_df_RS, df_finviz_prfm, stock)
        s_list_count += 1

    # print("*********************")
    # print(master_data)

    return render_template('watchlist.html',
        jalerts_data = json.dumps(alert_data),
        jstocks_data = json.dumps(master_data),
    )

@app.route('/industry', methods=['GET', 'POST'])
def industry():
    print('industry')
    sort_by = "daily"
    if request.method == "GET":
        _url = urlparse(request.url) #get url
        _query = _url.query #get the variable part of the url
        _str = _query.split('&') #split if there is more than one variable
        for _section in _str:
            _split_section = _section.split('=') #split 
            if _split_section[0]=='sortby':
                sort_by = unquote(_split_section[1])

    _gcharts = gcharts.IndustryCharts()
    _gcharts.getData(sort_by)
    master_data = ""
    master_data = _gcharts.build_maser_data()
    print(master_data)
    # send all to industry.html page
    return render_template('industry.html', 
        jindustry_data = json.dumps(master_data)
    )

@app.route('/stocks', methods=['GET', 'POST'])
def stocks():
    print('stocks')
    stocklist = ['AAPL'] #default stock
    industry_dropdown = ''
    action_by = 'Stocks'
    
    if request.method == "GET":
        _url = urlparse(request.url) #get url
        _query = _url.query #get the variable part of the url
        _str = _query.split('&') #split if there is more than one variable
        for _section in _str:
            _split_section = _section.split('=') #split 
            if _split_section[0]=='industry':
                industry_dropdown = unquote(_split_section[1])

    #If page if reloaded via form submit
    if request.method == "POST":
        stocklist = request.form['stocklist'].replace(" ", "").upper().split(',')
        industry_dropdown = request.form['industry_dropdown']

    if len(industry_dropdown) > 0:
        _list = db_calls.select_ticker_by_industry(industry_dropdown)
        stocklist = _list
        action_by = 'Industry - ' + industry_dropdown

    _gcharts = gcharts.GlobalCharts()
    _gcharts.getHistoricalData(stocklist)
    _gcharts.build_list(stocklist)
    master_data = _gcharts.build_master_data(stocklist)
    master_rsdata = _gcharts.build_master_rsdata(stocklist)

    # print(master_data)
    # send all to stocks.html page
    return render_template('stocks.html', 
        jstocks_data = json.dumps(master_data),
        jrs_data = json.dumps(master_rsdata),
        jaction_by = json.dumps(action_by)
    )

