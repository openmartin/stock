# -*- coding: utf-8 -*-
import os
import sys
from stock_analysis.models import StockTradeDay, StockCode
from datetime import date, datetime, timedelta
from stock_datagather.http_datagather import get_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

#当天的交易记录
if __name__ == '__main__':
    corp_list = StockCode.objects.all()
    #end_date = datetime.today()
    end_date = date(2014, 4, 1)
    end_date_str = end_date.strftime('%Y%m%d')
    start_date = end_date
    start_date_str = start_date.strftime('%Y%m%d')
    
    print start_date_str, end_date_str
    
    for corp in corp_list:
        get_data(corp.corp_code, start_date_str, end_date_str)