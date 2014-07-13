# -*- coding: utf-8 -*-
import re
#判断证券代码的类型
#股票 STOCK  600 601    000 001 002
#ETF基金 ETF 510        1599*
#企业债 CORPBOND 120 122 124     111 112
#可转债 CONVERBOND 110 113   125 126 127 128
#
def code_kind(code):
    STOCK_p = re.compile('^600*|^601*|^000*|^001*|^002*')
    ETF_p = re.compile('^510*|^1599*')
    CORPBOND_p = re.compile('^120*|^122*|^124*|^111*|^112*')
    CONVERBOND_p = re.compile('^110*|^113*|^125*|^126*|^127*|^128*')
    
    if STOCK_p.match(code):
        return 'STOCK'
    elif ETF_p.match(code):
        return 'ETF'
    elif CORPBOND_p.match(code):
        return 'CORPBOND'
    elif CONVERBOND_p.match(code):
        return 'CONVERBOND'
    else:
        return None
    
def money_round(x):
    if isinstance(x, float):
        return round(x,2)
    elif isinstance(x, int):
        return round(float(x),2)
    