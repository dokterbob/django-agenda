from datetime import datetime

from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext

from django.conf import settings

from django.contrib.auth.models import User

from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager

from django.contrib.sitemaps import ping_google

class Location(models.Model):
    class Meta:
        verbose_name = _('location')
        verbose_name_plural = _('locations')
        ordering = ('title',)
    
    def __unicode__(self):
        return self.title
        
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), db_index=True)
    
    address = models.CharField(_('address'), max_length=255, blank=True)

class PublicationManager(CurrentSiteManager):
    def get_query_set(self):
        return super(CurrentSiteManager, self).get_query_set().filter(publish=True, publish_date__lte=datetime.now())

class Event(models.Model):
    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')
        ordering = ['-event_date', '-start_time', '-title']
        get_latest_by = 'event_date'
        permissions = (("change_author", ugettext("Change author")),)
        unique_together = ("event_date", "slug")

    def __unicode__(self):
        return _("%(title)s on %(event_date)s") % { 'title'      : self.title,
                                                    'event_date' : self.event_date }

    @models.permalink                                               
    def get_absolute_url(self):
        return ('agenda-detail', (), {
                  'year'  : self.event_date.year, 
                  'month' : self.event_date.month, 
                  'day'   : self.event_date.day, 
                  'slug'  : self.slug })
        
    objects = models.Manager()
    on_site = CurrentSiteManager()
    published = PublicationManager()

    # Core fields
    title = models.CharField(_('title'), max_length=255)
    slug = models.SlugField(_('slug'), db_index=True)
    
    event_date = models.DateField(_('date'))
    
    start_time = models.TimeField(_('start time'), blank=True, null=True)
    end_time = models.TimeField(_('end time'), blank=True, null=True)
    
    location = models.ForeignKey(Location, blank=True, null=True)

    description = models.TextField(_('description'))

    # Extra fields
    add_date = models.DateTimeField(_('add date'),auto_now_add=True)
    mod_date = models.DateTimeField(_('modification date'), auto_now=True)
    
    author = models.ForeignKey(User, verbose_name=_('author'), db_index=True)

    publish_date = models.DateTimeField(_('publication date'), default=datetime.now())
    publish = models.BooleanField(_('publish'), default=True)
    
    allow_comments = models.BooleanField(_('Allow comments'), default=True)

    sites = models.ManyToManyField(Site)
    
    def save(self):
        super(Event, self).save()
        if not settings.DEBUG:
            try:
                ping_google()
            except Exception:
                import logging
                logging.warn('Google ping on save did not work.')

