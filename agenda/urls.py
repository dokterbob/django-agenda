from django.conf.urls.defaults import *
#from django.conf import settings

from models import *

info_dict = {
    'queryset'    : Event.published.all(),
    'date_field'  : 'event_date'
}

urlpatterns = patterns('agenda.views.date_based',
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[-\w]+)/$', 'object_detail', info_dict),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',                  'archive',       info_dict),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',                                   'archive',       info_dict),
    (r'^(?P<year>\d{4})/$',                                                      'archive',       info_dict),
    (r'^$',                                                                      'index',         info_dict),
)
