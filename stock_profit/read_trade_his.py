# -*- coding: utf-8 -*-
import os
import sys
from datetime import datetime, date
import csv
from stock_analysis.models import StockTradeRecord
from stock_analysis.utils import money_round

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")

# 证券买入
# 证券卖出
# 股息入帐
# 红股入帐
# 股息红利税补
# 新股入帐
def map_operation(chs):
    if chs == u'证券买入':
        return 'B'
    elif chs == u'证券卖出':
        return 'S'
    elif chs == u'股息入帐':
        return 'P'
    elif chs == u'红股入帐':
        return 'H'
    elif chs == u'股息红利税补':
        return 'D'
    elif chs == u'新股入帐':
        return 'N'
    else: #其他的情况不处理
        return None



def read_trade_his(file_path):
    reader = csv.reader(open(file_path, "rb"), delimiter='\t', quoting=csv.QUOTE_NONE)
    headers = reader.next()
    for row in  reader:
        st = StockTradeRecord()
        st.trandt = datetime.strptime(row[0], '%Y%m%d')#成交日期
        st.deal_time = datetime.strptime(row[1], '%H:%M:%S')#成交时间
        st.corp_code = row[2]#证券代码
        st.corp_name = row[3]#证券名称
        st.trade_type = map_operation(row[4])#操作
        st.trade_amount = int(row[5])#成交数量
        st.trade_price = money_round(float(row[6]))#成交均价
        st.trade_value = money_round(float(row[7]))#成交金额
        st.commission_fee = money_round(float(row[8]))#手续费
        st.stamp_tax = money_round(float(row[9]))#印花税
        st.transfer_fee = money_round(float(row[10]))#过户费
        st.total_balance = money_round(float(row[11]))#发生金额
        row[12]#成交编号
        row[13]#合同编号
        row[14]#备注
        row[15]#股东帐户
        row[16]#交易市场
        st.total_fee_tax = money_round(float(row[8])+float(row[9])+float(row[10]))
        if not st.trade_type == None:
            st.save()



if __name__ == '__main__':
    file_path = u'E:\\py_workspace\\stock\\stock_profit\\交割单20140712.txt'
    read_trade_his(file_path)