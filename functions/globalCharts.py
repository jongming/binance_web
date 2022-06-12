import imp
import db_calls
import pandas as pd


def appendDF(_df1, _df2): #append two dataFrames into one dataFrames
        _df = pd.DataFrame()
        _df = pd.concat([_df1, _df2], axis=0)
        return _df

def build_stock_list(name, stocklist):
    #build stock_list dynamically based on number of tickers. stock_list = ['','',''] 
    _jstock_list = []
    for x in range(len(stocklist)):
        # _listItem = 'stock'+str(x+1)
        _listItem = name+str(x)
        _jstock_list.append(_listItem)   
    print("***********_jstock_list****************")
    print(_jstock_list)
    print("***********_jstock_list****************")
    return _jstock_list

def process_alert_data(ticker, df):
        _processed_data = {}
        _ticker = []
        _price = []
        _open_date = []
        _triggered_date = []
        _close = []
        for _record in df.values:
            _ticker.append(ticker)
            _price.append(_record[1])
            _open_date.append(_record[2])
            _triggered_date.append(_record[3])
            _close.append(_record[4])
        _processed_data['ticker'] = _ticker
        _processed_data['price'] = _price
        _processed_data['open_date'] = _open_date
        _processed_data['triggered_date'] = _triggered_date
        _processed_data['close'] = _close
        return _processed_data

def process_data(df, ticker): #build data structure for Tradingview chart
        print(">>>>>>>>>>>>>>>>>>process_data<<<<<<<<<<<<<<")
        print(df)
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

def process_rsdata(df, df_finviz_prfm, ticker): #build data structor for chartjs and info section
        processed_rs = {}
        p_date = []
        p_CMP = [] 
        p_EPS = []
        p_RS = []
        p_SMR = []
        p_SMR_value = []
        p_AD = []
        p_AD_value = []
        _iindustry = ''
        _sector = ''
        _findustry = ''
        _find_dwm = ''
        df.reset_index(inplace=True)
        for _rs in df.values:
            _date = _rs[1] 
            _CMP = _rs[2]
            _EPS = _rs[3]
            _RS = _rs[4]
            _SMR = _rs[5]
            _SMR_value = _rs[6]
            _AD = _rs[7]
            _AD_value = _rs[8]
            _iindustry = _rs[9].capitalize()
            _sector = _rs[10]
            _findustry = _rs[11]
            _find_dwm = df_finviz_prfm.loc[df_finviz_prfm['industry'] == _findustry]
            
            p_date.append(_date)
            p_CMP.append(_CMP)
            p_EPS.append(_EPS)
            p_RS.append(_RS)
            p_SMR.append(_SMR)
            p_SMR_value.append(_SMR_value)
            p_AD.append(_AD)
            p_AD_value.append(_AD_value)
 
        processed_rs['ticker'] = ticker
        processed_rs['iindustry'] = _iindustry
        processed_rs['sector'] = _sector
        processed_rs['findustry'] = _findustry
        processed_rs['date'] = p_date
        processed_rs['cmp'] = p_CMP
        processed_rs['eps'] = p_EPS
        processed_rs['rs'] = p_RS
        processed_rs['smr'] = p_SMR
        processed_rs['smr_value'] = p_SMR_value
        processed_rs['ad'] = p_AD
        processed_rs['ad_value'] = p_AD_value
        if (len(_find_dwm) > 0):
            processed_rs['find_dwn'] = _find_dwm.reset_index().values.tolist()
        else:
            processed_rs['find_dwn'] = ['']
        # print(processed_rs)
        return processed_rs

def process_finviz_data(df_daily, ind, df_tickers):
        processed_data = {}
        p_date =[]
        p_perfT = []
        for _data in df_daily.values:
            p_date.append(_data[0])
            p_perfT.append(_data[2])
        processed_data['industry'] = ind
        processed_data['on_date'] = p_date
        processed_data['perfT'] = p_perfT
        processed_data['stocks'] =  df_tickers.to_dict('record')
        return processed_data

def process_hist_data(df_daily, ind, df_tickers):
        processed_data = {}
        p_date =[]
        p_close = []
        for _data in df_daily.values:
            p_date.append(_data[0])
            p_close.append(_data[3])
        processed_data['industry'] = ind
        processed_data['on_date'] = p_date
        processed_data['close'] = p_close
        processed_data['stocks'] =  df_tickers.to_dict('record')
        return processed_data

def is_consolidating(df, lookback=15, pcent = 2):
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

def is_breaking_out(df, lookback=15, pcent = 2):
        lookback = int(lookback)
        pcent = int(pcent)
        _last_close = df[-1:]['adj_close'].values
        #is stock consolidating up to but not including the most recent close 
        if is_consolidating(df[:-1], lookback=lookback, pcent=pcent):
            #get records not including most recent close
            recent_closes = df[(lookback+1)*-1:-1]
            if _last_close > recent_closes['adj_close'].max():
                return True
        return False

def save_df_csv(df, file, isUpdate=False):
    try:
        if isUpdate:    
            df.to_csv(file, mode='a', header=False, index=False) #update CSV
        else:
            df.to_csv(file, mode='w', index=False) #Save (overwrite) CSV
    except: 
        print("Error while saving")

def read_csv(file, columns):
    _ls = pd.read_csv(file, engine='python')
    _df = pd.DataFrame(_ls, columns=columns)
    return _df

class GlobalCharts:
    def __init__(self):
        self.df = pd.DataFrame()
        self.df_historicalData = pd.DataFrame()
        # self.stocklist = stocklist
        self.jstock_list = []

    def getHistoricalData(self, stocklist):
        #Get all historical data from tickers
        _df_merged_stocks = pd.DataFrame()
        for stock in stocklist:
            ticker = ''.join(stock)
            # print("++++++++++++++")
            # print(ticker)
            # print(str(type(ticker)))
            _df_stocks = db_calls.select_historical_data(ticker, 180)
            # print(_df_stocks)
            _df_merged_stocks = appendDF(_df_merged_stocks, _df_stocks)
        self.df_historicalData = _df_merged_stocks
        return _df_merged_stocks
        # print(self.df_stocks)
        # return df_stocks

    def getHistoricalData_fromcsv(self, file, columns):
        _df = read_csv(file, columns)
        print("******************")
        print(_df)
        print("******************")
        self.df_historicalData = _df
        return _df

    def getVolumeChange(self, cmp, rs, price_change, volume_percent, volume):
        df = db_calls.select_IBD_tickers_byVariables(cmp, rs, price_change, volume_percent, volume)
        return df

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
            _is_consolidating = is_consolidating(_df, lookback = lookback, pcent=pcent)
            _is_breaking_out = is_breaking_out(_df, lookback = lookback, pcent=pcent)
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

    def historicalData_to_cvs(self, file):
        save_df_csv(self.df_historicalData, file, False)

    def build_list(self, stocklist):
        self.jstock_list = build_stock_list('stock', stocklist)
        print("0000000jstock_list000000000")
        print(self.jstock_list)

    def build_master_rsdata(self, stocklist):
        #Get industry performance data
        _df_finviz_prfm = db_calls.select_Finviz_Performance_data()
        _master_rsdata = {}
        _count = 0    
        #build merge all data structure into master_rsdata
        for stock in stocklist:
            # print(">>>>>>>>>>>>>>>>> " + stock)
            _df_RS = db_calls.select_IBD_data(stock)
            # print(_df_RS)
            # print("-----------------------")
            _master_rsdata[self.jstock_list[_count]] = process_rsdata(_df_RS, _df_finviz_prfm, stock)
            _count += 1
        return _master_rsdata

    def build_master_data(self, stocklist):
        #build merge all data structure into master_data
        _count = 0
        _master_data = {}
        for stock in stocklist:
            _master_data[self.jstock_list[_count]] = process_data(self.df_historicalData, stock)
            _count += 1
        return _master_data


class IndustryCharts:
    def __init__(self) -> None:
        self.df_finviz_daily_performance = pd.DataFrame()
        self.df_ticker_industry = pd.DataFrame()
        self.ind_list = []

    def getData(self, sort_by):
        
        _df = pd.DataFrame()
        _industry_list = db_calls.select_Finviz_Performance(sort_by)
        for _ind in list(_industry_list):
            # _ind = re.sub('\W+', '', _ind)
            _ind = "".join(_ind) #_ind is a tuple, extract just the string
            # _df_r = db_calls.select_Finviz_Performance_industry(_ind)
            _df_r = db_calls.select_historical_industry_performance(_ind)
            _df = pd.concat([_df_r, _df], ignore_index=True)
        
        self.df_finviz_daily_performance = _df
        print("+++++++++++++++++")
        print(self.df_finviz_daily_performance)
        self.df_ticker_industry = db_calls.select_ticker_and_industry()

    def build_maser_data(self):
        _ind_list = build_stock_list("ind", self.df_finviz_daily_performance.index)
        _master_data = {}
        _count = 0
        for ind in list(self.df_finviz_daily_performance.industry.unique()):
            _df_daily = self.df_finviz_daily_performance[self.df_finviz_daily_performance.industry == ind]
            _df_tickers = self.df_ticker_industry[self.df_ticker_industry.industry == ind]
            # _master_data[_ind_list[_count]] = process_finviz_data(_df_daily, ind, _df_tickers)
            _master_data[_ind_list[_count]] = process_hist_data(_df_daily, ind, _df_tickers)
            _count+=1
        return _master_data