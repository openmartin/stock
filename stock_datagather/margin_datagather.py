# -*- coding: utf-8 -*-

import os
import sys
from string import Template
import csv
import requests
from datetime import date, datetime
from stock_analysis.models import StockTradeDay
import xlrd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

#http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk20140716.xls
#http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&amp;CATALOGID=1837_xxpl&amp;TABKEY=tab2&amp;ENCODE=1&amp;txtDate=2014-07-16
#http://www.csf.com.cn/IAutoDisclosure/file/margin20140717.xls

#上交所 XLS
def sse_margin_datagather(trandt):
    pass

#深交所 XML
def szse_margin_datagather(trandt):
    pass

#转融通 XLS
def csf_margin_datagather(trandt):
    pass




