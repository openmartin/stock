# -*- coding: utf-8 -*-
import os
import sys
from string import Template
import csv
import requests
from datetime import date, datetime
from stock_analysis.models import StockTradeDay

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_analysis.settings")
#URL
#http://quotes.money.163.com/service/chddata.html?code=0600000&start=19991110&end=20140328&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP

URL_TEMPLATE = 'http://quotes.money.163.com/service/chddata.html?code=$corp_code&start=$start_date&end=$end_date&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER;TCAP;MCAP'
TEMP_PATH = 'temp'

#download cvs
def down_trande_csv(corp_code, start_date, end_date):
    if corp_code[0] == '6':
        corp_code = '0' + corp_code
    elif corp_code[0] == '0':
        corp_code = '1' + corp_code
    elif corp_code[0] == '3':
        corp_code = '1' + corp_code
    csv_tpl = Template(URL_TEMPLATE)
    csv_url = csv_tpl.substitute(corp_code=corp_code, start_date=start_date, end_date=end_date)
    r = requests.post(csv_url)
    
    f_path = os.path.join(TEMP_PATH, corp_code)
    f_path = f_path + '.csv'
    f = open(f_path, 'wb')
    f.write(r.content)
    f_abspath = os.path.abspath(f_path)
    f.close()
    return f_abspath

#import csv to database
def import_csv(file_path):
    csv_file = open(file_path, 'rb')
    reader = csv.reader(csv_file)
    headers = next(reader)
    for line in reader:
        print line
        if line[3] == '0.0':
            continue
        trade_day = StockTradeDay()
        trade_day.trandt = datetime.strptime(line[0], '%Y-%m-%d')
        trade_day.corp_code = line[1][1:]
        trade_day.corp_name = line[2].decode('GB18030')
        trade_day.close_price = float(line[3])
        trade_day.high_price = float(line[4])
        trade_day.low_price = float(line[5])
        trade_day.open_price = float(line[6])
        trade_day.pre_close_price = float(line[7])
        trade_day.change_amount = float(line[8])
        trade_day.change_rate = float(line[9])
        trade_day.turnover_rate = float(line[10])
        trade_day.turnover_amount = float(line[11])
        trade_day.turnover_money = float(line[12])
        trade_day.total_value = float(line[13])
        trade_day.market_value = float(line[14])
        trade_day.save()


def get_data(corp_code, start_date, end_date):
    file_path = down_trande_csv(corp_code, start_date, end_date)
    import_csv(file_path)

if __name__ == '__main__':
    get_data('600000', '20140328', '20140328')