"""event URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from events import views as ev
from pageant import views as pv
from auth import views as av

urlpatterns = [
    url(r'^$', ev.home, name='home'),
    # url(r'^events/', include(foo.urls')),
    url(r'^event/(?P<event_id>[0-9]+)', ev.event, name='event'),
    url(r'^pageant/(?P<pageant_id>[0-9]+)', pv.pageant, name='pageant'),
    url(r'^pageant_process/(?P<pageant_id>[0-9]+)', pv.pageant_process, name='pageant_process'),
    url(r'^pageant_overall/(?P<pageant_id>[0-9]+)/(?P<group_id>[0-9]+)', pv.all_ratings, name='pageant_overall'),
    url(r'^event_raw/(?P<event_id>[0-9]+)', ev.raw, name='event_raw'),
    url(r'^participant/(?P<participant_id>[0-9]+)', ev.participant, name='participant'),
    url(r'^login/$', av.login, name='login'),
    url(r'^logout/$', av.logout, name='logout'),
    url(r'^admin/', admin.site.urls),
    #url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
   # url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]
