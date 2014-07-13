# -*- coding: utf-8 -*-
import os
import sys
from stock_analysis.models import StockTradeDay, StockCode, StockTurnoverAnalysis
from datetime import date, datetime
from stock_datagather.data_analysis import corp_analysis
from stock_datagather.day_increment import get_data

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

def deleteBeforeRun(trandt):
    StockTradeDay.objects.filter(trandt=trandt).delete()
    StockTurnoverAnalysis.objects.filter(trandt=trandt).delete()
    
def runTrandt(trandt):
    deleteBeforeRun(trandt)
    end_date = trandt
    end_date_str = end_date.strftime('%Y%m%d')
    start_date = end_date
    start_date_str = start_date.strftime('%Y%m%d')
    corp_list = StockCode.objects.all()
    for corp in corp_list:
        get_data(corp.corp_code, start_date_str, end_date_str)
        corp_analysis(trandt, corp.corp_code, corp.corp_name)
    

if __name__ == '__main__':
    trandt = date(2014, 6, 13)
    #trandt = date.today()
    runTrandt(trandt)
    