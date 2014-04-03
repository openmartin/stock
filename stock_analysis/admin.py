# -*- coding: utf-8 -*-
from django.contrib import admin
from stock_analysis.models import StockTradeDay, StockCode

admin.site.register(StockCode)
admin.site.register(StockTradeDay)