# -*- coding: utf-8 -*-
import os
import sys
from string import Template
import csv
from  xml.dom  import  minidom
import requests
from datetime import date, datetime, timedelta
from stock_analysis.models import StockTradeDay, StockMarginTrading, StockCsfMarginTrading, StockCsfMarginTotal
import xlrd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

TEMP_PATH = 'temp'

#http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk20140716.xls
#http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&amp;CATALOGID=1837_xxpl&amp;TABKEY=tab2&amp;ENCODE=1&amp;txtDate=2014-07-16
#http://www.csf.com.cn/IAutoDisclosure/file/margin20140717.xls

#上交所 XLS
def sse_margin_datagather(trandt):
    URL_TEMPLATE = 'http://www.sse.com.cn/market/dealingdata/overview/margin/a/rzrqjygk$trandt.xls'
    margin_tpl = Template(URL_TEMPLATE)
    margin_url = margin_tpl.substitute(trandt=trandt.strftime('%Y%m%d'))
    r = requests.post(margin_url)
    
    f_path = os.path.join(TEMP_PATH, 'sse_margin')
    f_path = f_path + '.xls'
    f = open(f_path, 'wb')
    f.write(r.content)
    f_abspath = os.path.abspath(f_path)
    f.close()
    
    margin_workbook = xlrd.open_workbook(f_path)
    margin_detail_sheet = margin_workbook.sheet_by_name(u'明细信息')
    
    for row in range(1, margin_detail_sheet.nrows):
        corp_code = margin_detail_sheet.cell(row, 0).value
        corp_name = margin_detail_sheet.cell(row, 1).value
        rzye = margin_detail_sheet.cell(row, 2).value #融资余额
        rzmre = margin_detail_sheet.cell(row, 3).value #融资买入额
        rzche = margin_detail_sheet.cell(row, 4).value #融资偿还额
        rqyl = margin_detail_sheet.cell(row, 5).value #融券余量
        rqmcl = margin_detail_sheet.cell(row, 6).value #融券卖出量
        rqchl = margin_detail_sheet.cell(row, 7).value #融券偿还额
        
        margin_trade = StockMarginTrading()
        margin_trade.trandt = trandt
        margin_trade.corp_code = corp_code
        margin_trade.corp_name = corp_name
        margin_trade.rzye = rzye
        margin_trade.rzmre = rzmre
        margin_trade.rzche = rzche
        margin_trade.rqyl = rqyl
        margin_trade.rqmcl = rqmcl
        margin_trade.rqchl = rqchl
        margin_trade.save()

#深交所 XML
def szse_margin_datagather(trandt):
    headers = {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Encoding':'gzip, deflate',
                   'Accept-Language':'zh-cn,zh;q=0.8,en-us;q=0.5,en;q=0.3',
                   'Host':'58.56.98.78:8801',
                   'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:17.0) Gecko/20100101 Firefox/17.0',
                   'Host':'www.szse.cn',
                   'Referer':'http://www.szse.cn/main/disclosure/rzrqxx/rzrqjy/'}
    
    URL_TEMPLATE = 'http://www.szse.cn/szseWeb/FrontController.szse?ACTIONID=8&CATALOGID=1837_xxpl&TABKEY=tab2&ENCODE=1&txtDate=$trandt'
    margin_tpl = Template(URL_TEMPLATE)
    margin_url = margin_tpl.substitute(trandt=trandt.strftime('%Y-%m-%d'))
    r = requests.post(margin_url, headers = headers)
    
    f_path = os.path.join(TEMP_PATH, 'szse_margin')
    f_path = f_path + '.xls'
    f = open(f_path, 'wb')
    f.write(r.content)
    f_abspath = os.path.abspath(f_path)
    f.close()
    
    f = open(f_path)
    f_head = f.readline()
    xml_str = f.readline()
    f.close()
    f_tail = """<table id='tbl-data-bottom-line'  height='2' cellSpacing='0' cellPadding='0'  width="100%" bgColor='#b8d9ec' border='0'><tr><td></td></tr></table>"""
    nPos = xml_str.index(f_tail)
    
    xml_str = xml_str[0:nPos]
    doc = minidom.parseString(xml_str.decode('GBK'))
    
    
    tr_l = doc.documentElement.getElementsByTagName('tr')
    for tr in tr_l:
        if tr.getElementsByTagName('td')[0].firstChild.nodeValue == u'证券代码':
            continue
        
        corp_code = tr.getElementsByTagName('td')[0].firstChild.nodeValue
        corp_name = tr.getElementsByTagName('td')[1].firstChild.nodeValue
        rzmre = tr.getElementsByTagName('td')[2].firstChild.nodeValue #融资买入额(元)
        rzye = tr.getElementsByTagName('td')[3].firstChild.nodeValue #融资余额(元)
        rqmcl = tr.getElementsByTagName('td')[4].firstChild.nodeValue #融券卖出量(股)
        rqyl = tr.getElementsByTagName('td')[5].firstChild.nodeValue #融券余量(股)
        rqylje = tr.getElementsByTagName('td')[6].firstChild.nodeValue #融券余额(元)
        rzrqjyzl = tr.getElementsByTagName('td')[7].firstChild.nodeValue #融资融券余额(元)
        
        rzmre = clean_num(rzmre)
        rzye = clean_num(rzye)
        rqmcl = clean_num(rqmcl)
        rqyl = clean_num(rqyl)
        rqylje = clean_num(rqylje)
        rzrqjyzl = clean_num(rzrqjyzl)
        
        margin_trade = StockMarginTrading()
        margin_trade.trandt = trandt
        margin_trade.corp_code = corp_code
        margin_trade.corp_name = corp_name
        margin_trade.rzye = rzye
        margin_trade.rzmre = rzmre
        margin_trade.rqyl = rqyl
        margin_trade.rqmcl = rqmcl
        margin_trade.rqylje = rqylje
        margin_trade.rzrqjyzl = rzrqjyzl
        margin_trade.save()
        

#转融通 XLS
def csf_margin_datagather(trandt):
    URL_TEMPLATE = 'http://www.csf.com.cn/IAutoDisclosure/file/margin$trandt.xls'
    csf_margin_tpl = Template(URL_TEMPLATE)
    csf_margin_url = csf_margin_tpl.substitute(trandt=trandt.strftime('%Y%m%d'))
    r = requests.post(csf_margin_url)
    
    f_path = os.path.join(TEMP_PATH, 'csf_margin')
    f_path = f_path + '.xls'
    f = open(f_path, 'wb')
    f.write(r.content)
    f_abspath = os.path.abspath(f_path)
    f.close()
    
    csf_margin_workbook = xlrd.open_workbook(f_path)
    csf_margin_detail_sheet = csf_margin_workbook.sheet_by_name(u'转融券交易明细')
    
    for row in range(2, csf_margin_detail_sheet.nrows):
        corp_code = csf_margin_detail_sheet.cell(row, 1).value
        corp_name = csf_margin_detail_sheet.cell(row, 2).value
        csf_margin_type = csf_margin_detail_sheet.cell(row, 3).value #转融券期限
        rlsl = csf_margin_detail_sheet.cell(row, 4).value #转融券融入数量(万股)
        rcsl = csf_margin_detail_sheet.cell(row, 5).value #转融券融出数量(万股)
        
        if corp_code == u'小计':
            continue
        if csf_margin_detail_sheet.cell(row, 0).value == u'合计':
            continue
        
        csf_margin_trade = StockCsfMarginTrading()
        csf_margin_trade.trandt = trandt
        csf_margin_trade.corp_code = corp_code
        csf_margin_trade.corp_name = corp_name
        csf_margin_trade.csf_margin_type = translate_dict('csf_margin_type', csf_margin_type)
        csf_margin_trade.rlsl = rlsl
        csf_margin_trade.rcsl = rcsl
        csf_margin_trade.save()
    
    csf_margin_total_sheet = csf_margin_workbook.sheet_by_name(u'转融券交易汇总')
    for row in range(2, csf_margin_total_sheet.nrows):
        corp_code = csf_margin_total_sheet.cell(row, 1).value
        corp_name = csf_margin_total_sheet.cell(row, 2).value
        qcsl = csf_margin_total_sheet.cell(row, 3).value #期初余量(万股)
        rcsl = csf_margin_total_sheet.cell(row, 4).value #转融券融出数量(万股)
        qmsl = csf_margin_total_sheet.cell(row, 5).value #期末余量(万股)
        qmye = csf_margin_total_sheet.cell(row, 6).value #期末余额(万元)
        
        if corp_code == u'小计':
            continue
        if csf_margin_total_sheet.cell(row, 0).value == u'合计':
            continue
        
        qcsl = clean_num(qcsl)
        rcsl = clean_num(rcsl)
        qmsl = clean_num(qmsl)
        qmye = clean_num(qmye)
        
        csf_margin_total = StockCsfMarginTotal()
        csf_margin_total.trandt = trandt
        csf_margin_total.corp_code = corp_code
        csf_margin_total.corp_name = corp_name
        csf_margin_total.qcsl = qcsl
        csf_margin_total.rcsl = rcsl
        csf_margin_total.qmsl = qmsl
        csf_margin_total.qmye = qmye
        csf_margin_total.save()

def translate_dict(dict_type, dict_str):
    if dict_type == 'csf_margin_type':
        if dict_str == u'3天':
            return '003'
        if dict_str == u'7天':
            return '007'
        if dict_str == u'14天':
            return '014'
        if dict_str == u'28天':
            return '028'
        if dict_str == u'91天':
            return '091'
        if dict_str == u'182天':
            return '182'

def clean_num(num):
    if num == u'-':
        return 0.0
    
    nPos = None
    try:
        nPos = num.index(',')
    except ValueError:
        pass
    
    if not nPos == None:
        num = num.replace(',', '')
        return num
    else:
        return num
    

def after_clean_data(trandt):
    #sse 补全 融券余量金额 融资融券余额
    #融券余量金额 = 融券余量 * 收盘价
    #融资融券余额 = 融资余额 + 融券余量金额
    yestoday = trandt - timedelta(days=1)
    today_margin_l = StockMarginTrading.objects.filter(trandt=trandt).\
        filter(corp_code__startswith='60')
    yestoday_margin_l = StockMarginTrading.objects.filter(trandt=trandt).\
        filter(corp_code__startswith='60')
    for a_margin in today_margin_l:
        for b_margin in yestoday_margin_l:
            pass
    
    #szse 补全 融券偿还量 融资偿还额
    #融券卖出量 - 融券偿还量 = 今日融券余量 - 昨日融券余量
    #融券偿还量 = 昨日融券余量 - 今日融券余量 + 融券卖出量
    #融资买入额 - 融资偿还额 = 今日融资余额 - 昨日融资余额
    #融资偿还额 = 昨日融资余额 - 今日融资余额 + 融资买入额
    
    

if __name__ == '__main__':
    trandt = date(2014, 6, 13)
    sse_margin_datagather(trandt)
    csf_margin_datagather(trandt)
    szse_margin_datagather(trandt)
    
