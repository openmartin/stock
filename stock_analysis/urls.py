from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'stock_analysis.views.home', name='home'),
    # url(r'^stock_analysis/', include('stock_analysis.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'stock_analysis.views.index', name='index'),
    url(r'^refinacing$', 'stock_analysis.views.refinacing', name='refinacing'),
    url(r'^securities_borrowing/(?P<code>(\d+))/$', 'stock_analysis.views.borrowing', name='securities_borrowing'),
    url(r'^margin/(?P<code>(\d+))/$', 'stock_analysis.views.margin', name='margin'),
    url(r'^securities_lending/(?P<code>(\d+))/$', 'stock_analysis.views.lending', name='securities_lending'),
    url(r'^about/$', 'stock_analysis.views.about', name='about')
)
