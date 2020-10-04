from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.shortcuts import render
import finnhub
import time
import logging
import mpld3
from datetime import datetime as dt, timedelta
from datetime import date as de
import datetime
import os
from .settings import *
import requests
import json
from . import fix_messages, fix_mapping
import ipdb
from w_app.models import TradeData
from w_app.serializers import TradeDataSerializer

finnhub_client = finnhub.Client(api_key=api_key)

def getNews(symbol):
    today = de.today()
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
    # ipdb.set_trace()
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

def getOrderDetails(req):
    #http://localhost:8000/blotter/?name=&_TraderId=123&_Side=Buy&_OrderType=Market&_Quantity=1&_Price=1
    traderid = req.GET['_TraderId']
    side = req.GET['_Side']
    ordertype = req.GET['_OrderType']
    qty = req.GET['_Quantity']
    price = req.GET['_Price']
    ordertype = fix_mapping.OrderType.get(ordertype)
    side = fix_mapping.Side.get(side)
    fix_message = fix_messages.createNewOrderSinge('FB', side, ordertype, qty)
    trade_data = TradeData(fix=fix_message,
                            symbol='FB',
                            quantity=qty,
                            order_type=ordertype,
                            direction=side,
                            exec_date=datetime.datetime.now())
    trade_data.save()
    return render(req, 'execute.html', {'tradeid': traderid,
                                     'side':side,
                                     'ordertype':ordertype,
                                     'qty':qty,
                                     'price':price,
                                     'fix_message':fix_message
                                                        })

@csrf_exempt
def trade_list(req):
    """
    List all code snippets, or create a new snippet.
    """
    if req.method == 'GET':
        snippets = TradeData.objects.all()
        serializer = TradeDataSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif req.method == 'POST':
        data = JSONParser().parse(req)
        serializer = TradeDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def trade_detail(request, pk):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = TradeData.objects.get(pk=pk)
    except TradeData.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TradeDataSerializer(snippet)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TradeDataSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
