# -*- coding: utf-8 -*-
import os
import sys
from stock_analysis.models import StockTradeDay, StockCode
from datetime import date, datetime, timedelta
from stock_datagather.http_datagather import get_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

def init_one_corp(corp_code):
    end_date = datetime.today()
    end_date_str = end_date.strftime('%Y%m%d')
    start_date = end_date - timedelta(days=120)
    start_date_str = start_date.strftime('%Y%m%d')
    
    print start_date_str, end_date_str
    
    get_data(corp.corp_code, start_date_str, end_date_str)

if __name__ == '__main__':
    corp_list = StockCode.objects.all()
    end_date = datetime.today()
    end_date_str = end_date.strftime('%Y%m%d')
    start_date = end_date - timedelta(days=120)
    start_date_str = start_date.strftime('%Y%m%d')
    
    print start_date_str, end_date_str
    
    for corp in corp_list:
        get_data(corp.corp_code, start_date_str, end_date_str)