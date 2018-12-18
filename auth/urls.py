from django.conf.urls.defaults import *
from django.contrib import *

urlpatterns = patterns('',  
    url(r'^recover/$', 'spmcAuth.views.recover'),
    url(r'^logout/$', 'spmcAuth.views.logout'),
    url(r'^login/$', 'spmcAuth.views.login'),
)
