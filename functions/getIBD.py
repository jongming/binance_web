import pandas as pd
from matplotlib.pyplot import cla
import requests
import bs4
import re
import sqlite3
import traceback
import sys
import datetime
from functions import error_handler as er
import db_calls

class GetIBD:
    def __init__(self):
        self.masterRecord = []

    def _addZeros(self, vol):
        newVol = 0
        if (vol.endswith('m')):
            #print(f'old_vol:{vol}')
            newVol = float(vol.replace('m','')) * 1000000
            #print(f'new_vol:{newVol}')
        else:
            newVol = float(vol) * 1000000
        return newVol      

    def _buildRecord(self, soup):
        sectors = soup.select('.expandable')
        filtertxt = ('Rtg', 'IPO')
        sectxt = ''
        masterRecord = []
        for sector in sectors:
            sectxt = re.sub('\d+. ', '', sector.find('h3').text, 1) #Get the sector name
            try:
                for row in sector.find('table').tr.next_siblings:   
                    if type(row) is not bs4.element.NavigableString:
                        record = []
                        for tr in row:
                            if tr.text.startswith(filtertxt):
                                break
                            else:
                                record.append(tr.text)

                        record.append(sectxt[0:sectxt.find(' ')])
                        masterRecord.append(record)
            except Exception as e:
                print(f'Error: {e}') 
        return masterRecord

    def _cleanGrade(self, txt):
        _txt = ''
        if txt == '..' or txt == '':
            _txt = 0
        else:
            _txt = txt.strip()
        return _txt

    def _cleanName(self, txt):
        return re.sub(r'\d+\.\d+|\xa0', '', txt)

    def _removeR(self, txt):
        if txt.startswith('r'):
            x = txt[txt.rindex('r')+2:] + ''
            #print(f'x:{x}')
            return x
        else:
            return txt

    def _pe_cleaner(self, pe):
        if pe.isnumeric():
            return pe
        return ''

    def _appendDF(self, _df1, _df2): #append two dataFrames into one dataFrames
        _df = pd.DataFrame()
        _df = pd.concat([_df1, _df2], axis=0)
        return _df

    def _buildRecord(self, soup):
        sectors = soup.select('.expandable')
        filtertxt = ('Rtg', 'IPO')
        sectxt = ''
        masterRecord = []
        for sector in sectors:
            sectxt = re.sub('\d+. ', '', sector.find('h3').text, 1) #Get the sector name
            try:
                for row in sector.find('table').tr.next_siblings:   
                    if type(row) is not bs4.element.NavigableString:
                        record = []
                        for tr in row:
                            if tr.text.startswith(filtertxt):
                                break
                            else:
                                record.append(tr.text)

                        record.append(sectxt[0:sectxt.find(' ')])
                        masterRecord.append(record)
            except Exception as e:
                print(f'Error: {e}') 
        return masterRecord

    def _list_to_df(self, date, masterRecord):
        _df_main = pd.DataFrame()
        _df_stock = pd.DataFrame()
        for r in masterRecord:
            if len(r) == 15:
                _composit = r[0]
                _eps = r[1]
                _rs = r[2]
                _smr = self._cleanGrade(r[3])
                _accdis = self._cleanGrade(r[4])
                _fiftytwowk = r[5]
                _name = self._cleanName(r[6])
                _ticker = self._removeR(r[7])
                _price = r[8]
                _change = r[9]
                _vol_percent = r[10]
                _volume = round(self._addZeros(r[11]))
                _pe = self._pe_cleaner(r[12])
                _industry = r[14]
                _on_date = date

                _data1 = [_ticker, _composit, _eps, _rs, _smr, _accdis, _fiftytwowk, _price, _change, _vol_percent, _volume, _pe, _on_date]        
                _df = pd.DataFrame([_data1], columns = ['ticker', 'composit', 'eps', 'rs', 'SMR', 'accdis', '52wk', 'price', 'change', 'vol_percent', 'volume', 'pe', 'on_date'])
                _df_main = self._appendDF(_df_main, _df)
                
                _today = datetime.datetime.now().strftime('%Y-%m-%d')
                _data2 = [_ticker, _name, _industry, _today, _ticker]
                _df1 = pd.DataFrame([_data2], columns = ['ticker', 'name', 'industry', 'date_added','ticker'])
                _df_stock = self._appendDF(_df_stock, _df1)
        return [_df_main, _df_stock]

    def scrape_IBD_data(self, _date):
        # print('get_IBD_data: ' + str(_date))
        # print(type(_date))
        # print('day: ' + _date[-2:])
        # print('month: ' + _date[5:7])
        # print('year: ' + _date[0:4])
        _day = _date[-2:]
        _month = _date[5:7]
        _year = _date[0:4]
        monthDict = {'01':'jan', '02':'feb', '03':'mar', '04':'apr', '05':'may', '06':'jun', '07':'jul', '08':'aug', '09':'sep', '10':'oct', '11':'nov', '12':'dec'}
        strDate = f"{monthDict[_month]}-{_day}-{_year}"
        # print('strDate: ' + strDate)
        try:
            url = f'https://www.investors.com/data-tables/ibd-smart-nyse-nasdaq-tables-{strDate}/'
            # print("url: "+ url)
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        except Exception as error:
            _error = er.Error_Handler(error, sys.exc_info())
            _error.save_to_errorlog(">>> Failed: select_alerts")

        try:
            response = requests.get(url, headers=headers)
            soup = bs4.BeautifulSoup(response.text, 'lxml')
        except Exception as error:
            print('*****error 1')
            print("Exception class is: ", error.__class__)
            print("Exception is", error.args)
            print('Printing detailed SQLite exception traceback: ')
            exc_type, exc_value, exc_tb = sys.exc_info()
            print(traceback.format_exception(exc_type, exc_value, exc_tb))

        self.masterRecord = self._buildRecord(soup)
             
    def save_IBD_data(self, date):
        if (db_calls.if_IBD_daily_exist(date)):
            print('Record already exist')
        else:
            _rs_data, _stocks_data = self._list_to_df(date, self.masterRecord)
            db_calls.save_IBD_daily(date, _rs_data, _stocks_data)

    def get_IBD_data(self, date):
        return db_calls.select_IBD_data_byDate(date)