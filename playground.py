
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
# # for a in r.json()[0:11]:
# #     print(a.get('displaySymbol'))
# #print(r.json()[0].get('currency'))
#
# ls = [a.get('symbol') for a in r.json()]
# print(ls)



r = requests.get('https://finnhub.io/api/v1/news?category=general&token=bsf2pnfrh5rf0ieh0s00')
news = r.json()[:6]


# print(news[0].get('headline'))

from datetime import date, timedelta

today = date.today()
lastweek = today-timedelta(days=7)
r = requests.get('https://finnhub.io/api/v1/company-news?symbol={}&from={}&to={}&token={}'.format('AAPL', lastweek, today, api_key))
news = r.json()[:6]
print(news)
