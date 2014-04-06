# -*- coding: utf-8 -*-
from django.db import models
import datetime
from django.utils import timezone
from django.utils.translation import ugettext as _

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
    

