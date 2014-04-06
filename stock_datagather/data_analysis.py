# -*- coding: utf-8 -*-
import os
import sys
from datetime import date, datetime, timedelta
from stock_analysis.models import StockTradeDay, StockCode, StockTurnoverAnalysis
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

ANA_GO_STEP = 5
DAYS_SIZE_LIST = [1,2,3,4,5,10]

def corp_analysis(trandt, corp_code, corp_name):
    stock_turnover_ana = StockTurnoverAnalysis()
    for days_size in DAYS_SIZE_LIST:
        if days_size == 1:
            try:
                one_rate = day_analysis(trandt, corp_code, days_size)
            except IndexError:
                one_rate = 0.0
        elif days_size == 2:
            try:
                two_rate = day_analysis(trandt, corp_code, days_size)
            except IndexError:
                two_rate = 0.0
        elif days_size == 3:
            try:
                three_rate = day_analysis(trandt, corp_code, days_size)
            except IndexError:
                three_rate = 0.0
        elif days_size == 4:
            try:
                four_rate = day_analysis(trandt, corp_code, days_size)
            except IndexError:
                four_rate = 0.0
        elif days_size == 5:
            try:
                five_rate = day_analysis(trandt, corp_code, days_size)
            except IndexError:
                five_rate = 0.0
        elif days_size == 10:
            try:
                ten_rate = day_analysis(trandt, corp_code, days_size)
            except IndexError:
                ten_rate = 0.0
    
    if one_rate == None:
        pass
    else:
        stock_turnover_ana.trandt = trandt
        stock_turnover_ana.corp_code = corp_code
        stock_turnover_ana.corp_name = corp_name
        stock_turnover_ana.one_rate = one_rate
        stock_turnover_ana.two_rate = two_rate
        stock_turnover_ana.threee_rate = three_rate
        stock_turnover_ana.four_rate = four_rate
        stock_turnover_ana.five_rate = five_rate
        stock_turnover_ana.ten_rate = ten_rate
        stock_turnover_ana.save()

def day_analysis(trandt, corp_code, days_size):
    his_trade = StockTradeDay.objects.filter(corp_code=corp_code).order_by('-trandt')[0:60]
    
    if trandt == his_trade[0].trandt:
        pass
    else:
        return None
    
    a = float(0)
    for j in range(days_size):
        a =  a + his_trade[j].turnover_rate
    
    b_list = []
    for i in range(ANA_GO_STEP):
        b = float(0)
        for k in range(days_size):
            print (i+1)*days_size+k
            b = b + his_trade[(i+1)*days_size+k].turnover_rate
        b_list.append(b)
    
    print a
    print b_list
    return a/(sum(b_list)/ANA_GO_STEP)

if __name__ == '__main__':
    #1,2,3,4,5 天的成交额是前几个单位时间的多少倍
    trandt = date(2014, 3, 28)
    corp_analysis(trandt, '600000', '浦发银行')