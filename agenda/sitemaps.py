from django.contrib.sitemaps import Sitemap

from models import Event

from django.contrib.comments.models import Comment

class EventSitemap(Sitemap):
    changefreq = "daily"
    
    def items(self):
        return Event.published.all()
    
    def lastmod(self, obj):
        """ The Event 'changes' when there are newer comments, so check for that. """
        
        if obj.allow_comments:
            try:
                comment_date = Comment.objects.for_model(Event).filter(object_pk=obj.id).latest('submit_date').submit_date
                return comment_date > obj.mod_date and comment_date or obj.mod_date
            except Comment.DoesNotExist:
                pass
        
        return obj.mod_date
            
