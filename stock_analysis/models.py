# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone

class StockCode(models.Model):
    corp_code=models.CharField(max_length=20)
    corp_name=models.CharField(max_length=200)

class StockTradeDay(models.Model):
    trandt = models.DateField()
    corp_code = models.CharField(max_length=20)
    corp_name = models.CharField(max_length=200)
    close_price = models.FloatField()     #收盘价
    high_price = models.FloatField()      #最高价
    low_price = models.FloatField()       #最低价
    open_price = models.FloatField()      #开盘价
    pre_close_price = models.FloatField() #前收盘价
    change_amount = models.FloatField() #涨跌额
    change_rate = models.FloatField()   #涨跌幅
    turnover_rate = models.FloatField() #换手率
    turnover_amount = models.FloatField() #成交量
    turnover_money  = models.FloatField() #成交额
    total_value = models.FloatField()  #总市值
    market_value = models.FloatField() #流通市值


class StockCashFlowDay(models.Model):
    trandt = models.DateField()
    close_price = models.FloatField()     #收盘价
    change_rate = models.FloatField()     #涨跌幅
    turnover_rate = models.FloatField()   #换手率
    inflow = models.FloatField()          #资金流入
    outflow = models.FloatField()         #资金流出
    net_inflow = models.FloatField()      #净流入
    main_inflow = models.FloatField()     #主力流入
    main_outflow = models.FloatField()    #主力流出
    main_net_inflow  = models.FloatField()#主力净流入
    
class StockTurnoverAnalysis(models.Model):
    trandt = models.DateField()
    corp_code = models.CharField(max_length=20)
    corp_name = models.CharField(max_length=200)
    one_rate = models.FloatField()
    two_rate = models.FloatField()
    threee_rate = models.FloatField()
    four_rate = models.FloatField()
    five_rate = models.FloatField()
    
    
