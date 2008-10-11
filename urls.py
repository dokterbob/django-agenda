from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

if settings.DEBUG:
    from os import path
    urlpatterns = patterns('django.views', (r'^static/(?P<path>.*)$', 'static.serve', {'document_root': path.join(settings.PROJECT_ROOT, 'static') }))
else:
    urlpatterns = patterns('')

urlpatterns += patterns('',
    #(r'^/', include('foo.urls')),

    # Django Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root)
)
