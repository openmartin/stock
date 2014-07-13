# -*- coding: utf-8 -*-
import os
import sys
from stock_analysis.models import StockTradeDay, StockCode, StockTurnoverAnalysis
from datetime import date, datetime, timedelta
from stock_datagather.http_datagather import get_data
from stock_datagather.data_analysis import corp_analysis

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

def gatherdata_one_corp(corp_code):
    end_date = datetime.today()
    end_date_str = end_date.strftime('%Y%m%d')
    start_date = end_date - timedelta(days=120)
    start_date_str = start_date.strftime('%Y%m%d')
    
    print start_date_str, end_date_str
    
    get_data(corp_code, start_date_str, end_date_str)
    
def analysis_one_corp(corp_code, corp_name):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=10)
    for i in range(11):
        i_date = start_date + timedelta(days=i)
        corp_analysis(i_date, corp_code, corp_name)
        

if __name__ == '__main__':
    #trandt = date(2014, 5, 5)
    trandt = date.today()
    #deleteBeforeRun(trandt)
    corp_list = [
        ['600104','上汽集团'],
        ['002019','鑫富药业'],
        ['600256','广汇能源'],
        ['600597','光明乳业'],
        ['002500','山西证券'],
        ['000049','德赛电池'],
        ['002681','奋达科技'],
        ['600834','申通地铁'],
        ['600823','世茂股份'],
        ['601231','环旭电子'],
        ['601766','中国南车'],
        ]
    
    for one_corp in corp_list:
        corp_code = one_corp[0]
        corp_name = one_corp[1]
        StockCode.objects.filter(corp_code=corp_code).delete()
        StockTradeDay.objects.filter(corp_code=corp_code).delete()
        StockTurnoverAnalysis.objects.filter(corp_code=corp_code).delete()
        
    
    for one_corp in corp_list:
        corp_code = one_corp[0]
        corp_name = one_corp[1]
        
        #save stock_code
        stock_code = StockCode()
        stock_code.corp_code=corp_code
        stock_code.corp_name=corp_name
        stock_code.save()
        
        gatherdata_one_corp(corp_code)
        analysis_one_corp(corp_code, corp_name)
    