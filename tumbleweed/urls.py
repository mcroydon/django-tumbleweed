from django.conf.urls.defaults import *
from tumbleweed.views import tumble, archive_year, archive_month, archive_day

urlpatterns = patterns('tumbleweed.views',
    url(r'^$', tumble, name='tumbleweed_tumble'),
    url(r'^(?P<year>\d{4})/$', archive_year, name='tumbleweed_archive_year'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$', archive_month, name='tumbleweed_archive_month'),
    url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\d{2})/$', archive_day, name='tumbleweed_archive_day'),
)