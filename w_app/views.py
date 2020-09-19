from django.http import HttpResponse as hr
from django.shortcuts import render
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.pyplot import figure
import finnhub
import time
import logging
import mpld3
from datetime import datetime as dt
from datetime import date as de
from datetime import timedelta as td
import datetime
import os
from .settings import *
import requests
import json

finnhub_client = finnhub.Client(api_key=api_key)

def getNews(symbol):
    today = date.today()
    lastweek = today-timedelta(days=7)
    r = requests.get('https://finnhub.io/api/v1/company-news?symbol={}&from={}&to={}&token={}'.format(symbol, lastweek, today, api_key))

    news = r.json()[:6]
    headline = [a.get('headline') for a in news]
    link = [a.get('url') for a in news]
    image = [a.get('image') for a in news]
    newz = list(zip(headline, link, image))

    return newz

def time_converter(dttime):
    splitted = dttime.split('-')
    year = int(splitted[0])
    month = int(splitted[1])
    day = int(splitted[2])
    d = datetime.date(year,month,day)
    unixtime = time.mktime(d.timetuple())
    logging.info('Converted {} into unixtime of {}'.format(dttime, unixtime))
    return str(int(unixtime))

def Home(req):
    newz = getNews('AAPL')
    return render(req,'home.html', {'newz':newz})

def Quote(req):

    stock = req.GET['symbol']
    newz = getNews(stock)
    r = requests.get('https://finnhub.io/api/v1/quote?symbol={}&token={}'.format(stock,api_key))
    quote = r.json()
    open = quote.get('o')
    close = quote.get('c')
    high = quote.get('h')
    low = quote.get('l')
    pc = quote.get('pc')
    return render(req,'quote.html', {'open':open, 'close':close, 'high':high, 'low':low, 'pc':pc, 'newz':newz, 'symbol':stock})
    # NEED TO ADD TIME TOO



def Count(req):
    pass

def DispayChart(req):

    start = time_converter(req.GET['startdate'])
    end = time_converter(req.GET['enddate'])
    stock = str(req.GET['stock'])
    res = finnhub_client.stock_candles(stock, 'D', start, end)
    dt = pd.DataFrame(res)

    dt['time'] = dt['t'].astype(int)
    timeStamp = [datetime.fromtimestamp(a) for a in dt['time']]
    fig = go.Figure(data=[
                go.Candlestick(x=timeStamp,
                open=dt['o'],
                high=dt['h'],
                low=dt['l'],
                close=dt['c'],
                )])
    fig.update_layout(title_text="{}: {}-{}".format(stock, timeStamp[0], timeStamp[-1]),
                  title_font_size=30)
    try:
        os.remove('templates/myfig.html')
    except:
        pass
    fig.write_html('templates/myfig.html')
    return render(req,'myfig.html')
