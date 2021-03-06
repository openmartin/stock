# -*- coding: utf-8 -*-
from django.contrib import admin
from stock_analysis.models import *

class StockCodeAdmin(admin.ModelAdmin):
    fields = ('corp_code', 'corp_name')
    list_display = ('corp_code', 'corp_name')
    list_display_links = ('corp_code', 'corp_name')
    ordering = ('corp_code',)
    
    
class StockTradeDayAdmin(admin.ModelAdmin):
    date_hierarchy = 'trandt'
    list_per_page = 100
    ordering = ('-trandt', 'corp_code')
    #fields = ('trandt','corp_code','corp_name','close_price','high_price','low_price',
    #          'open_price','pre_close_price','change_amount','change_rate',)
    list_display = ('trandt','corp_code','corp_name','close_price','high_price','low_price',
              'open_price','pre_close_price','change_amount','change_rate',)
    list_display_links = ('trandt', 'corp_code', 'corp_name')
    list_filter = ('trandt',)
    search_fields = ['corp_code', 'corp_name']
    
class StockTurnoverAnalysisAdmin(admin.ModelAdmin):
    date_hierarchy = 'trandt'
    list_per_page = 100
    ordering = ('-trandt', '-one_rate')
    #fields = ('pname', 'pdept' , 'isvalid', 'remark')
    list_display = ('trandt','corp_code','corp_name','one_rate','two_rate',
                    'threee_rate','four_rate','five_rate','ten_rate')
    list_display_links = ('trandt', 'corp_code', 'corp_name')
    list_filter = ('trandt',)
    search_fields = ['corp_code', 'corp_name']


class StockTradeRecordAdmin(admin.ModelAdmin):
    date_hierarchy = 'trandt'
    list_per_page = 100
    ordering = ('-trandt',)
    list_display = ('trandt','corp_code','corp_name','trade_type','trade_amount',
                    'trade_price','trade_value','total_fee_tax','total_balance')
    list_display_links = ('trandt', 'corp_code', 'corp_name')
    list_filter = ('trandt',)
    search_fields = ['corp_code', 'corp_name']
    fields = ('trandt','corp_code','corp_name','trade_type','trade_amount',
                    'trade_price')

class StockHolderAdmin(admin.ModelAdmin):
    list_per_page = 100
    search_fields = ['corp_code', 'corp_name']
    fields = ('trandt','corp_code','corp_name','hold_amount','hold_price',
                    'balance_sell_price')

class StockProfitAdmin(admin.ModelAdmin):
    pass



admin.site.register(StockCode, StockCodeAdmin)
admin.site.register(StockTradeDay, StockTradeDayAdmin)
admin.site.register(StockTurnoverAnalysis, StockTurnoverAnalysisAdmin)
admin.site.register(StockTradeRecord, StockTradeRecordAdmin)
admin.site.register(StockHolder, StockHolderAdmin)
admin.site.register(StockProfit, StockProfitAdmin)
