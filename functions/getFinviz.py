from pandas_datareader import data as pdr
import pandas as pd
from datetime import date, time, timedelta
import datetime as dt
# import sqlite3
# import sys
# import traceback
from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import numpy as np
import requests
import bs4
import re
# from app import index
import db_calls

save_txt = 'data/save.txt'

class GetFinviz:
    def __init__(self) -> None:
        pass

    def _finviz_scraper(self, url):
        html = ""
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            webpage = urlopen(req).read()
            html = soup(webpage, "html.parser")
        except BaseException as err:
            print(f"Unexpected_finviz_scraper:  {err=}, {type(err)=}, {url}")
        return html

    def _company_info(self, html, ticker):
        name = ""
        sector = ""
        country = ""
        try:
            pd_fullview = pd.read_html(str(html), attrs = {'class': 'fullview-title'})[0]
            name = pd_fullview.values[1][0].strip()
            sector = pd_fullview.values[2][0].split("|")[0].strip()
            industry = pd_fullview.values[2][0].split("|")[1].strip()
            country = pd_fullview.values[2][0].split("|")[2].strip()
        except BaseException as err:
            print(f"Unexpected_company_info: {err=}, {type(err)=}, {ticker}")
        
        return ticker, name, sector, industry, country

    def _inside_buying(self, html, tag):
        try:   
            data = []
            for a in html.find_all('tr', {"class": tag}):
                row = []
                for b in a.find_all('td'):
                    row.append(b.text)
                data.append(row)
        except Exception as e:
            return e
        
        return data

    def tickers_notin_Finviz(self):
        return db_calls.select_IBD_tickers_notin_Finviz()

    def scrape_stock_info(self, df_tickers):
        df_all = pd.DataFrame()
        for ticker in df_tickers['ticker'].tolist():
            url = ("https://finviz.com/quote.ashx?t=" + ticker)
            html = self._finviz_scraper(url)
            if len(html) > 0:
                company_info = self._company_info(html, ticker)
                # print(company_info)
                column_names = ['ticker', 'name', 'sector', 'industry', 'country']
                df = pd.DataFrame([company_info], columns=column_names)
                # print(df)
                df_all = pd.concat([df_all, df], axis=0)
        
        df_all['ticker2'] = df_all.loc[:, 'ticker']
        # print(df_all)
        return df_all

    def scrape_inside_buying(self):
        from operator import itemgetter
        df = pd.DataFrame()
        record = []

        url = ("https://finviz.com/insidertrading.ashx?tc=1")
        html = self._finviz_scraper(url)
        if len(html) > 0:
            _tag1 = "insider-buy-row-1 cursor-pointer align-top"
            _tag2 = "insider-buy-row-2 cursor-pointer align-top"

            _data1 = self._inside_buying(html, _tag1)
            _data2 = self._inside_buying(html, _tag2)
            _all_data = _data1 + _data2
            
            for row in sorted(_all_data, key=itemgetter(0)):
                record.append([row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[0], row[1], row[2], row[3], row[4], row[5], row[6]])

            column_names = ['ticker', 'owner', 'relationship', 'on_date', 'action', 'cost', 'shares', 'ticker', 'owner', 'relationship', 'on_date', 'action', 'cost', 'shares']
            df = pd.DataFrame(record, columns=column_names)
            # print(df)

        if record:
            db_calls.batch_insert_Finviz_inside_buying(df)
 
    
    def save_Finviz(self, df):
        # print(df)
        db_calls.batch_insert_Finviz(df)

    def scrape_daily_data(self):
        url = f'https://finviz.com/groups.ashx?g=industry&v=210'
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "DNT": "1", "Connection": "close", "Upgrade-Insecure-Requests": "1"}
        response = requests.get(url, headers=headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        with open(save_txt, 'w+') as f:
            f.write(str(soup))

        strFind = []
        pattern = re.compile(r'ticker')
        with open (save_txt, 'rt') as save_txt_file: #look for 'ticker' in file line by line
            for line_in_file in save_txt_file:
                if pattern.search(line_in_file) != None:
                    strFind.append(line_in_file)

        match = re.search('\{(.*)\}', strFind[1])
        strGroup = match.group(1)
        lst = strGroup.split('},')

        mainList = []
        _date = (dt.datetime.now() - timedelta(1)).strftime('%Y-%m-%d')

        for item in lst:
            newList = []
            r1 = item.replace('","','"|"') #replace quotes and comma with |
            r1 = r1.replace('"','') #remove double quotes
            r2 = r1.split('|') #split by commas
            inlist = r2[4].split(',')

            newList.append(_date)
            newList.append(r2[1].split(':')[1]) #industry
            newList.append(inlist[0].split(':')[1]) #perfT
            newList.append(inlist[1].split(':')[1]) #perfW
            newList.append(inlist[2].split(':')[1]) #perfM
            newList.append(r2[1].split(':')[1]) #industry
            newList.append(_date)
            mainList.append(newList)

        df = pd.DataFrame(mainList, columns = ['date', 'industry', 'perfT', 'perfW', 'perfM', 'industry', 'date'])
        self._save_date(df)

    def _save_date(self, df):
        # print(df)
        db_calls.batch_insert_Finviz_r_perform(df)

    def get_data(self):
        return db_calls.select_Finviz_Performance_data()


