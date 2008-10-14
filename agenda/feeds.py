import logging

from datetime import datetime, timedelta

from django.contrib.syndication.feeds import Feed
from django.contrib.sites.models import Site

from django.utils.translation import ugettext as _
from django.core.urlresolvers import reverse

from models import Event

class EventFeed(Feed):
    title = _('%s agenda' % Site.objects.get_current())
    description = _('Upcoming events in the agenda.')
    
    def link(self):
        return reverse('agenda-index')
    
    def items(self):
        return Event.published.filter(event_date__gte=datetime.now() - timedelta(days=1))
    
    def item_pubdate(self, item):
        return item.publish_date
    
