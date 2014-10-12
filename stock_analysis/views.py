# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, date, timedelta

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))

#转融资
def refinacing(request):
    return render_to_response("refinacing.html", {"current":"refinacing"
                                             },\
                  context_instance=RequestContext(request))

#转融券
def securities_borrowing(request):
    return render_to_response("securities_borrowing.html", {"current":"securities_borrowing"
                                             },\
                  context_instance=RequestContext(request))

#融资
def margin(request):
    return render_to_response("margin.html", {"current":"margin"
                                             },\
                  context_instance=RequestContext(request))

#融券
def securities_lending(request):
    return render_to_response("securities_lending.html", {"current":"securities_lending"
                                             },\
                  context_instance=RequestContext(request))
    
def about(request):
    return render_to_response("about.html", {"current":"about"
                                             },\
                  context_instance=RequestContext(request))
    
#根据参数不同，返回JSON格式的数据
def data_service(request):
    return ''

