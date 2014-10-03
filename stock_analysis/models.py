# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Count, Sum
from django.db.models.signals import pre_save, post_save
import datetime
from django.utils import timezone
from django.utils.translation import ugettext as _
import math
from utils import code_kind, money_round

BUY_OR_SELL = (
    ('B', '买入'),
    ('S', '卖出'),
    ('P', '股息入账'),
    ('B', '利税代扣'),  #一般都是债券,所以债券要在付息之前卖出
    ('N', '新股入账'),
    ('H', '红股入账'),
    ('D', '股息红利税补'),
)

#所有的费用四舍五入保留两位小数
#佣金率
COMMISSION_RATE = 2.0/10000
#印花税率
STAMP_TAX_RATE = 1.0/1000
#过户费
TRANSFER_RATE = 6.0/1000
#公司债企业债手续费
BOND_FEE_RATE = 5.0/100000
#可转债手续费
CONVERTIBLE_BOND_FEE_RATE = 8.0/100000


class StockCode(models.Model):
    corp_code=models.CharField(_('corp_code'), max_length=20)
    corp_name=models.CharField(_('corp_name'), max_length=200)
    
    class Meta:
        ordering = ['corp_code']
        verbose_name = _('StockCode')
        verbose_name_plural = _('StockCode')
    
    def __unicode__(self):
        return self.corp_name

class StockTradeDay(models.Model):
    trandt = models.DateField(_('trandt'))
    corp_code = models.CharField(_('corp_code'), max_length=20)
    corp_name = models.CharField(_('corp_name'), max_length=200)
    close_price = models.FloatField(_('close_price'))     #收盘价
    high_price = models.FloatField(_('high_price'))      #最高价
    low_price = models.FloatField(_('low_price'))       #最低价
    open_price = models.FloatField(_('open_price'))      #开盘价
    pre_close_price = models.FloatField(_('pre_close_price')) #前收盘价
    change_amount = models.FloatField(_('change_amount')) #涨跌额
    change_rate = models.FloatField(_('change_rate'))   #涨跌幅
    turnover_rate = models.FloatField(_('turnover_rate')) #换手率
    turnover_amount = models.FloatField(_('turnover_amount')) #成交量
    turnover_money  = models.FloatField(_('turnover_money')) #成交额
    total_value = models.FloatField(_('total_value'))  #总市值
    market_value = models.FloatField(_('market_value')) #流通市值
    
    class Meta:
        ordering = ['-trandt']
        verbose_name = _('StockTradeDay')
        verbose_name_plural = _('StockTradeDay')
    
    def __unicode__(self):
        return datetime.datetime.strftime(self.trandt, '%Y%m%d') + " " +self.corp_name
    

class StockCashFlowDay(models.Model):
    trandt = models.DateField(_('trandt'))
    close_price = models.FloatField(_('close_price'))     #收盘价
    change_rate = models.FloatField(_('change_rate'))     #涨跌幅
    turnover_rate = models.FloatField(_('turnover_rate'))   #换手率
    inflow = models.FloatField(_('inflow'))          #资金流入
    outflow = models.FloatField(_('outflow'))         #资金流出
    net_inflow = models.FloatField(_('net_inflow'))      #净流入
    main_inflow = models.FloatField(_('main_inflow'))     #主力流入
    main_outflow = models.FloatField(_('main_outflow'))    #主力流出
    main_net_inflow  = models.FloatField(_('main_net_inflow'))#主力净流入

    class Meta:
        ordering = ['-trandt']
        verbose_name = _('StockCashFlowDay')
        verbose_name_plural = _('StockCashFlowDay')

    def __unicode__(self):
        return datetime.datetime.strftime(self.trandt, '%Y%m%d') + " " +self.corp_name
    
class StockTurnoverAnalysis(models.Model):
    trandt = models.DateField(_('trandt'))
    corp_code = models.CharField(_('corp_code'), max_length=20)
    corp_name = models.CharField(_('corp_name'), max_length=200)
    one_rate = models.FloatField(_('one_rate'))
    two_rate = models.FloatField(_('two_rate'))
    threee_rate = models.FloatField(_('threee_rate'))
    four_rate = models.FloatField(_('four_rate'))
    five_rate = models.FloatField(_('five_rate'))
    ten_rate = models.FloatField(_('ten_rate'))

    class Meta:
        ordering = ['-trandt']
        verbose_name = _('StockTurnoverAnalysis')
        verbose_name_plural = _('StockTurnoverAnalysis')

    def __unicode__(self):
        return datetime.datetime.strftime(self.trandt, '%Y%m%d') + " " +self.corp_name

#融资融券信息
class StockMarginTrading(models.Model):
    trandt = models.DateField(_('trandt'))
    corp_code = models.CharField(_('corp_code'), max_length=20)
    corp_name = models.CharField(_('corp_name'), max_length=200)
    rqyl = models.FloatField('融券余量')          #融券余量
    rqmcl = models.FloatField('融券卖出量')       #融券卖出量
    rqchl = models.FloatField('融券偿还量', null=True, blank=True)       #融券偿还量
    rqylje  = models.FloatField('融券余量金额', null=True, blank=True)   #融券余量金额
    rzche  =  models.FloatField('融资偿还额', null=True, blank=True)     #融资偿还额
    rzmre  =  models.FloatField('融资买入额')     #融资买入额
    rzye = models.FloatField('融资余额')          #融资余额
    rzrqjyzl = models.FloatField('融资融券余额', null=True, blank=True)  #融资融券余额

#转融通业务
#转融券业务期限
CSF_MARGIN_TIME = (
    ('003', '3天'),
    ('007', '7天'),
    ('014', '14天'),
    ('028', '28天'),
    ('091', '91天'),
    ('182', '182天'),
)

class StockCsfMarginTrading(models.Model):
    trandt = models.DateField(_('trandt'))
    corp_code = models.CharField(_('corp_code'), max_length=20)
    corp_name = models.CharField(_('corp_name'), max_length=200)
    csf_margin_type = models.CharField('转融券期限', max_length=3, choices=CSF_MARGIN_TIME)
    rlsl = models.FloatField('转融券融入数量')     #转融券融入数量(万股)
    rcsl = models.FloatField('转融券融出数量')     #转融券融出数量(万股)

class StockCsfMarginTotal(models.Model):
    trandt = models.DateField(_('trandt'))
    corp_code = models.CharField(_('corp_code'), max_length=20)
    corp_name = models.CharField(_('corp_name'), max_length=200)
    qcsl = models.FloatField('期初余量')     #期初余量(万股)
    rcsl = models.FloatField('转融券融出数量')     #转融券融出数量(万股)
    qmsl = models.FloatField('期末余量')     #期末余量(万股)
    qmye = models.FloatField('期末余额')     #期末余额(万元)
    

#股票持仓
class StockHolder(models.Model):
    trandt = models.DateField(_('trandt')) #买入日期
    corp_code = models.CharField(_('corp_code'), max_length=20)
    corp_name = models.CharField(_('corp_name'), max_length=200)
    deal_time = models.TimeField('成交时间')
    hold_amount = models.IntegerField('数量')
    hold_price = models.FloatField('价格')
    hold_value = models.FloatField('总价')
    commission_fee = models.FloatField('佣金')
    stamp_tax = models.FloatField('印花税')
    transfer_fee = models.FloatField('过户费')
    total_fee_tax = models.FloatField('总费用')
    total_balance = models.FloatField('发生额')
    balance_sell_price = models.FloatField('不盈利卖出价', null=True, blank=True)
    

#股票交易记录
class StockTradeRecord(models.Model):
    trandt = models.DateField(_('trandt')) #买入/卖出日期
    corp_code = models.CharField(_('corp_code'), max_length=20)
    corp_name = models.CharField(_('corp_name'), max_length=200)
    deal_time = models.TimeField('成交时间')
    trade_type = models.CharField('买卖标志', max_length=1, choices=BUY_OR_SELL)
    trade_amount = models.IntegerField('数量')
    trade_price = models.FloatField('价格')
    trade_value = models.FloatField('总价')
    commission_fee = models.FloatField('佣金')
    stamp_tax = models.FloatField('印花税')
    transfer_fee = models.FloatField('过户费')
    total_fee_tax = models.FloatField('总费用')
    total_balance = models.FloatField('发生额')


#股票收益记录
class StockProfit(models.Model):
    corp_code = models.CharField(_('corp_code'), max_length=20, blank=True)
    corp_name = models.CharField(_('corp_name'), max_length=200, blank=True)
    buy_trandt = models.DateField('买入日期', null=True, blank=True)
    buy_trade_amount = models.IntegerField('买入数量', null=True, blank=True)
    buy_trade_price = models.FloatField('价格', null=True, blank=True)
    buy_trade_value = models.FloatField('总价', null=True, blank=True)
    buy_total_fee_tax = models.FloatField('总费用', null=True, blank=True)
    buy_total_balance = models.FloatField('发生额', null=True, blank=True)
    sell_trandt = models.DateField('卖出日期', null=True, blank=True)
    sell_trade_amount = models.IntegerField('数量', null=True, blank=True)
    sell_trade_price = models.FloatField('价格', null=True, blank=True)
    sell_trade_value = models.FloatField('总价', null=True, blank=True)
    sell_total_fee_tax = models.FloatField('总费用', null=True, blank=True)
    sell_total_balance = models.FloatField('发生额', null=True, blank=True)
    profit = models.FloatField('盈利', null=True, blank=True)
    profit_rate = models.FloatField('盈利率', null=True, blank=True)
    holde_days = models.IntegerField('持有天数', null=True, blank=True)
    remarks = models.CharField('备注', max_length=200, null=True, blank=True)
    
def PreSaveTradeRecord(sender, **kwargs): #计算佣金，印花税，过户费
    the_instance = kwargs['instance']
    corp_code = the_instance.corp_code
    trade_type = the_instance.trade_type
    trade_value = the_instance.trade_amount * the_instance.trade_price
    commission_fee = 0.0
    stamp_tax = 0.0
    transfer_fee = 0.0
    total_fee_tax = 0.0
    total_balance = 0.0
    code_kind_a = code_kind(corp_code)
    
    if code_kind_a == 'STOCK' or code_kind_a == 'ETF':
        commission_fee = trade_value * COMMISSION_RATE
        if commission_fee < 5.0:
            commission_fee = 5.0
    elif code_kind_a == 'CORPBOND':
        commission_fee = trade_value * BOND_FEE_RATE
    elif code_kind_a == 'CONVERBOND':
        commission_fee = trade_value * CONVERTIBLE_BOND_FEE_RATE
        

    if trade_type == 'B':
        if corp_code[0] == '6':
            transfer_fee = the_instance.trade_amount * TRANSFER_RATE
        if corp_code[0] == '0' or corp_code[0] == '3':
            transfer_fee = 0.0
        else:
            transfer_fee = 0.0
        
    elif trade_type == 'S':
        if code_kind_a == 'STOCK':
            stamp_tax = trade_value * STAMP_TAX_RATE
        else:
            stamp_tax = 0.0
        if corp_code[0] == '6':
            transfer_fee = the_instance.trade_amount * TRANSFER_RATE
        if corp_code[0] == '0' or corp_code[0] == '3':
            transfer_fee = 0.0
    
    commission_fee = money_round(commission_fee)
    stamp_tax = money_round(stamp_tax)
    transfer_fee = money_round(transfer_fee)
    total_fee_tax = money_round(commission_fee + stamp_tax + transfer_fee)
    total_balance = money_round(0.0 - trade_value - total_fee_tax)
    the_instance.commission_fee = commission_fee
    the_instance.stamp_tax = stamp_tax
    the_instance.transfer_fee = transfer_fee
    the_instance.total_fee_tax = total_fee_tax
    the_instance.total_balance = total_balance
    

def PostSaveTradeRecord(sender, **kwargs):#形成持仓记录和计算股票收益
    the_instance = kwargs['instance']
    code_kind_a = code_kind(the_instance.corp_code)
    if the_instance.trade_type == 'B':
        sh = StockHolder()
        sh.trandt = the_instance.trandt
        sh.corp_code = the_instance.corp_code
        sh.corp_name = the_instance.corp_name
        sh.deal_time = the_instance.deal_time
        sh.hold_amount = the_instance.trade_amount
        sh.hold_price = the_instance.trade_price
        sh.hold_value = the_instance.trade_value
        sh.commission_fee = the_instance.commission_fee
        sh.stamp_tax = the_instance.stamp_tax
        sh.transfer_fee = the_instance.transfer_fee
        sh.total_fee_tax = the_instance.total_fee_tax
        sh.total_balance = the_instance.total_balance
        
        sh.save()
        
    elif the_instance.trade_type == 'S':
        sell_amount = 0 - the_instance.trade_amount
        for sh in StockHolder.objects.filter(corp_code=the_instance.corp_code).\
             filter(trandt__lte=the_instance.trandt).\
             filter(hold_amount__gt=0).\
             order_by('trandt','deal_time'): #升序,先进先出法
            if sh.hold_amount > sell_amount:
                hold_sold_percent = sell_amount/float(sh.hold_amount)
                sold_sold_percent = sell_amount/float(0-the_instance.trade_amount)
                
                sp = StockProfit()
                sp.corp_code = sh.corp_code
                sp.corp_name = sh.corp_name
                sp.buy_trandt = sh.trandt
                sp.buy_trade_amount = sh.hold_amount
                sp.buy_trade_price = sh.hold_price
                sp.buy_trade_value = money_round(sh.hold_value * hold_sold_percent)
                sp.buy_total_fee_tax = money_round(sh.total_fee_tax * hold_sold_percent)
                sp.buy_total_balance = money_round(sh.total_balance * hold_sold_percent)
                sp.sell_trandt = the_instance.trandt
                sp.sell_trade_amount = the_instance.trade_amount
                sp.sell_trade_price = the_instance.trade_price
                sp.sell_trade_value = money_round(the_instance.trade_value * sold_sold_percent)
                sp.sell_total_fee_tax = money_round(the_instance.total_fee_tax * sold_sold_percent)
                sp.sell_total_balance = money_round(the_instance.total_balance * sold_sold_percent)
                sp.profit = the_instance.total_balance * sold_sold_percent + sh.total_balance * hold_sold_percent
                sp.profit_rate = (the_instance.total_balance * sold_sold_percent + sh.total_balance * hold_sold_percent)/sh.hold_value
                sp.holde_days = (the_instance.trandt.date() - sh.trandt).days
                sp.save()
                

                sh.hold_amount = sh.hold_amount - sell_amount
                sh.hold_value = money_round(sh.hold_value * (1.0-hold_sold_percent))
                sh.commission_fee = money_round(sh.commission_fee * (1.0-hold_sold_percent))
                sh.stamp_tax = money_round(sh.stamp_tax * (1.0-hold_sold_percent))
                sh.transfer_fee = money_round(sh.transfer_fee * (1.0-hold_sold_percent))
                sh.total_fee_tax = money_round(sh.total_fee_tax * (1.0-hold_sold_percent))
                sh.total_balance = money_round(sh.total_balance * (1.0-hold_sold_percent))
                sh.save()
                
                sell_amount = 0
                break
            elif sh.hold_amount < sell_amount:
                hold_sold_percent = sell_amount/float(sh.hold_amount)
                sold_sold_percent = sh.hold_amount/float(0-the_instance.trade_amount)
                
                sp = StockProfit()
                sp.corp_code = sh.corp_code
                sp.corp_name = sh.corp_name
                sp.buy_trandt = sh.trandt
                sp.buy_trade_amount = sh.hold_amount
                sp.buy_trade_price = sh.hold_price
                sp.buy_trade_value = sh.hold_value
                sp.buy_total_fee_tax = sh.total_fee_tax
                sp.buy_total_balance = sh.total_balance
                sp.sell_trandt = the_instance.trandt
                sp.sell_trade_amount = the_instance.trade_amount
                sp.sell_trade_price = the_instance.trade_price
                sp.sell_trade_value = the_instance.trade_value
                sp.sell_total_fee_tax = the_instance.total_fee_tax
                sp.sell_total_balance = the_instance.total_balance
                sp.profit = the_instance.total_balance * sold_sold_percent + sh.total_balance 
                sp.profit_rate = (the_instance.total_balance * sold_sold_percent + sh.total_balance)/sh.hold_value
                sp.holde_days = (the_instance.trandt.date() - sh.trandt).days
                sp.save()
                

                sh.hold_amount = 0
                sh.save()
                
                sell_amount = sell_amount - sh.hold_amount
            elif sh.hold_amount == sell_amount:
                
                
                sp = StockProfit()
                sp.corp_code = sh.corp_code
                sp.corp_name = sh.corp_name
                sp.buy_trandt = sh.trandt
                sp.buy_trade_amount = sh.hold_amount
                sp.buy_trade_price = sh.hold_price
                sp.buy_trade_value = sh.hold_value
                sp.buy_total_fee_tax = sh.total_fee_tax
                sp.buy_total_balance = sh.total_balance
                sp.sell_trandt = the_instance.trandt
                sp.sell_trade_amount = the_instance.trade_amount
                sp.sell_trade_price = the_instance.trade_price
                sp.sell_trade_value = the_instance.trade_value
                sp.sell_total_fee_tax = the_instance.total_fee_tax
                sp.sell_total_balance = the_instance.total_balance
                sp.profit = the_instance.total_balance + sh.total_balance
                sp.profit_rate = (the_instance.total_balance + sh.total_balance)/sh.hold_value
                sp.holde_days = (the_instance.trandt.date() - sh.trandt).days
                sp.save()
                
                sh.hold_amount = 0
                sh.save()
                
                sell_amount = 0
                break
            

    elif the_instance.trade_type == 'P':
        if code_kind_a == 'STOCK':
            sp = StockProfit()
            sp.corp_code = the_instance.corp_code
            sp.corp_name = the_instance.corp_code
            sp.profit = the_instance.total_balance
            sp.remarks = '股息入账'
            sp.save()
        if code_kind_a == 'ETF':
            sp = StockProfit()
            sp.corp_code = the_instance.corp_code
            sp.corp_name = the_instance.corp_code
            sp.profit = the_instance.total_balance
            sp.remarks = '股息入账'
            sp.save()
        elif code_kind_a == 'CORPBOND':
            sp = StockProfit()
            sp.corp_code = the_instance.corp_code
            sp.corp_name = the_instance.corp_code
            sp.profit = the_instance.total_balance
            sp.remarks = '股息入账'
            sp.save()
            sp2 = StockProfit()
            sp2.corp_code = the_instance.corp_code
            sp2.corp_name = the_instance.corp_code
            sp2.profit = money_round(0.0 - the_instance.total_balance * 0.2)
            sp2.remarks = '利税代扣'
            sp2.save()
        elif code_kind_a == 'CONVERBOND':
            sp = StockProfit()
            sp.corp_code = the_instance.corp_code
            sp.corp_name = the_instance.corp_code
            sp.profit = the_instance.total_balance
            sp.remarks = '股息入账'
            sp.save()
            sp2 = StockProfit()
            sp2.corp_code = the_instance.corp_code
            sp2.corp_name = the_instance.corp_code
            sp2.profit = money_round(0.0 - the_instance.total_balance * 0.2)
            sp2.remarks = '利税代扣'
            sp2.save()
        
    elif the_instance.trade_type == 'N': #新股入账
        sh = StockHolder()
        sh.trandt = the_instance.trandt
        sh.corp_code = the_instance.corp_code
        sh.corp_name = the_instance.corp_name
        sh.deal_time = the_instance.deal_time
        sh.hold_amount = the_instance.trade_amount
        sh.hold_price = the_instance.trade_price
        sh.hold_value = the_instance.trade_price * the_instance.trade_amount
        sh.commission_fee = the_instance.commission_fee
        sh.stamp_tax = the_instance.stamp_tax
        sh.transfer_fee = the_instance.transfer_fee
        sh.total_fee_tax = the_instance.total_fee_tax
        sh.total_balance = 0 - the_instance.trade_price * the_instance.trade_amount
        sh.save()
        
    elif the_instance.trade_type == 'H': #红股入账, 采用摊平成本方式
        total_amount = StockHolder.objects.filter(corp_code=the_instance.corp_code).\
             filter(trandt__lte=the_instance.trandt).\
             filter(hold_amount__gt=0).aggregate(Sum('hold_amount'))['hold_amount__sum']
        bonus_amount = the_instance.trade_amount
        for sh in StockHolder.objects.filter(corp_code=the_instance.corp_code).\
             filter(trandt__lte=the_instance.trandt).\
             filter(hold_amount__gt=0).\
             order_by('trandt','deal_time'): #升序,先进先出法
            bonus_percent = float(sh.hold_amount) / total_amount
            bonus_amount_a = int(round(bonus_percent * bonus_amount))
            sh.hold_amount = sh.hold_amount + bonus_amount_a
            sh.hold_price = sh.hold_value / sh.hold_amount
            sh.save()
            
    elif the_instance.trade_type == 'D': #股息红利税补
        sp = StockProfit()
        sp.profit = the_instance.total_balance
        sp.remarks = '股息红利税补'
        sp.save()
    else:
        pass


#pre_save.connect(PreSaveTradeRecord, sender=StockTradeRecord)
post_save.connect(PostSaveTradeRecord, sender=StockTradeRecord)

