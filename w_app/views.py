from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
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

@csrf_exempt
def getOrderDetails(req):

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
    print(req.body)
    # trade_data.save()
    return render(req, 'execute.html', {'tradeid': traderid,
                                     'side':side,
                                     'ordertype':ordertype,
                                     'qty':qty,
                                     'price':price,
                                     'fix_message':fix_message
                                                        })

@csrf_exempt
@api_view(['GET', 'POST'])
def trade_list(req, format=None):
    """
    List all code trades, or create a new trade.
    """
    if req.method == 'GET':
        snippets = TradeData.objects.all()
        serializer = TradeDataSerializer(snippets, many=True)
        return Response(serializer.data, status=200)

    elif req.method == 'POST':
        post_data = req.POST.dict()
        # ipdb.set_trace()
        """FIX IT LATER"""
        fix_message = fix_messages.createNewOrderSinge(
                req.POST['symbol'],
                req.POST['direction'],
                req.POST['order_type'],
                req.POST['quantity'])
        message = {'fix': fix_message.__str__(), 'exec_date': datetime.datetime.now()}
        post_data.update(message)
        # ipdb.set_trace()
        serializer = TradeDataSerializer(data=post_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
def trade_detail(request, pk, format=None):
    """
    Retrieve, update or delete a code snippet.
    """
    try:
        snippet = TradeData.objects.get(pk=pk)
    except TradeData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TradeDataSerializer(snippet)
        return Response(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TradeDataSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
