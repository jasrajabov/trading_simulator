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
from datetime import datetime as dt, date, timedelta
import os
import requests
import json
import finnhub
import json
api_key = 'bsf2pnfrh5rf0ieh0s00'
import datetime

finnhub_client = finnhub.Client(api_key=api_key)
# print(finnhub_client.quote('AAPL'))
#
# print(finnhub_client.aggregate_indicator('AAPL', 'D'))


import requests
r = requests.get('https://finnhub.io/api/v1/stock/symbol?exchange=US&token=bsf2pnfrh5rf0ieh0s00')
print(r.status_code)
# # for a in r.json()[0:11]:
# #     print(a.get('displaySymbol'))
# #print(r.json()[0].get('currency'))
#
# ls = [a.get('symbol') for a in r.json()]
# print(ls)



r = requests.get('https://finnhub.io/api/v1/news?category=general&token=bsf2pnfrh5rf0ieh0s00')
news = r.json()[:6]


# print(news[0].get('headline'))

today = date.today()
lastweek = today-timedelta(days=7)
r = requests.get('https://finnhub.io/api/v1/company-news?symbol={}&from={}&to={}&token={}'.format('AAPL', lastweek, today, api_key))
news = r.json()[:6]
print(news)



def time_converter(dttime):
    splitted = dttime.split('-')
    year = int(splitted[0])
    month = int(splitted[1])
    day = int(splitted[2])
    d = datetime.date(year,month,day)
    unixtime = time.mktime(d.timetuple())
    logging.info('Converted {} into unixtime of {}'.format(dttime, unixtime))
    print(unixtime)

time_converter('2020-01-01')
