from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

#from django.contrib import admin

#admin.site.unregister(FlatPage)

if settings.DEBUG:
    from os import path
    urlpatterns = patterns('django.views', (r'^static/(?P<path>.*)$', 'static.serve', {'document_root': path.join(settings.PROJECT_ROOT, 'static') }))
else:
    urlpatterns = patterns('')

urlpatterns += patterns('',
    #(r'^/', include('foo.urls')),
    (r'^tinymce/', include('tinymce.urls')),
    (r'^comments/', include('django.contrib.comments.urls')),

    # Django Admin
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/(.*)', admin.site.root)
)
