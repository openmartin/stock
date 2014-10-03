# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, redirect, render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime, date, timedelta

def index(request):
    return render_to_response("index.html", context_instance=RequestContext(request))