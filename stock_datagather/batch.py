# -*- coding: utf-8 -*-
import os
import sys
from stock_analysis.models import StockTradeDay, StockCode
from datetime import date, datetime
from stock_datagather.data_analysis import corp_analysis
from stock_datagather.day_increment import get_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

if __name__ == '__main__':
    trandt = date.today()
    end_date = trandt
    end_date_str = end_date.strftime('%Y%m%d')
    start_date = end_date
    start_date_str = start_date.strftime('%Y%m%d')
    corp_list = StockCode.objects.all()
    for corp in corp_list:
        get_data(corp.corp_code, start_date_str, end_date_str)
        corp_analysis(trandt, corp.corp_code, corp.corp_name)