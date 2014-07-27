# -*- coding: utf-8 -*-
import os
import sys
from  xml.dom  import  minidom
from stock_analysis.models import StockTradeDay, StockCode
import xlrd

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

my_stock = [
('002405','四维图新'),
('600036','招商银行'),
('002152','广电运通'),
('300104','乐视网  '),
('000001','平安银行'),
('000002','万  科Ａ'),
('002086','东方海洋'),
('000811','烟台冰轮'),
('601169','北京银行'),
('002439','启明星辰'),
('600660','福耀玻璃'),
('600060','海信电器'),
('600079','人福医药'),
('000333','美的集团'),
('000651','格力电器'),
('600690','青岛海尔'),
('600015','华夏银行'),
('600016','民生银行'),
('601818','光大银行'),
('000869','张  裕Ａ'),
('600221','海南航空'),
('002557','洽洽食品'),
('600887','伊利股份'),
('002142','宁波银行'),
('601519','大智慧  '),
('600332','白云山  '),
('601939','建设银行'),
('600300','维维股份'),
('002570','贝因美  '),
('002353','杰瑞股份'),
('600549','厦门钨业'),
('000338','潍柴动力'),
('601808','中海油服'),
('000702','正虹科技'),
('600050','中国联通'),
('002230','科大讯飞'),
('000848','承德露露'),
('002241','歌尔声学'),
('600000','浦发银行'),
('000584','友利控股'),
('600109','国金证券'),
('601628','中国人寿'),
('000488','晨鸣纸业'),
('601998','中信银行'),
('600606','金丰投资'),
('601601','中国太保'),
('000895','双汇发展'),
('600340','华夏幸福'),
('000858','五 粮 液'),
('000024','招商地产'),
('002603','以岭药业'),
('600055','华润万东'),
('600062','华润双鹤'),
('000999','华润三九'),
('000810','华润锦华'),
('000423','东阿阿胶'),
('600743','华远地产')]

# if __name__ == '__main__':
#     for stock in my_stock:
#         stock_code = StockCode()
#         stock_code.corp_code=stock[0]
#         stock_code.corp_name=stock[1]
#         stock_code.save()
        
if __name__ == '__main__':
    wb = xlrd.open_workbook(u'temp//margin20140717.xls')
    for s in wb.sheets():
        print 'Sheet:',s.name
    csf_margin_detail_sheet = wb.sheet_by_name(u'转融券交易明细')
    for row in range(0, csf_margin_detail_sheet.nrows):
        print csf_margin_detail_sheet.cell(row, 0).value
        print csf_margin_detail_sheet.cell(row, 1).value
        print csf_margin_detail_sheet.cell(row, 2).value
        print csf_margin_detail_sheet.cell(row, 3).value
        print csf_margin_detail_sheet.cell(row, 4).value
        print csf_margin_detail_sheet.cell(row, 5).value
#     f = open(u'temp//融资融券交易明细.xls')
#     f_head = f.readline()
#     xml_str = f.readline()
#     print xml_str
#     f_tail = """<table id='tbl-data-bottom-line'  height='2' cellSpacing='0' cellPadding='0'  width="100%" bgColor='#b8d9ec' border='0'><tr><td></td></tr></table>"""
#     nPos = xml_str.index(f_tail)
#     xml_str = xml_str[0:nPos]
#     print xml_str.decode('GBK')
#     doc = minidom.parseString(xml_str.decode('GBK'))
#     
#     f.close()
#     tr_l = doc.documentElement.getElementsByTagName('tr')
#     for tr in tr_l:
#         print tr.getElementsByTagName('td')[0].firstChild.nodeValue
#         print tr.getElementsByTagName('td')[1].firstChild.nodeValue
#         print tr.getElementsByTagName('td')[2].firstChild.nodeValue
#         print tr.getElementsByTagName('td')[3].firstChild.nodeValue
#         print tr.getElementsByTagName('td')[4].firstChild.nodeValue
#         print tr.getElementsByTagName('td')[5].firstChild.nodeValue
#         print tr.getElementsByTagName('td')[6].firstChild.nodeValue
#         print tr.getElementsByTagName('td')[7].firstChild.nodeValue
#         print
