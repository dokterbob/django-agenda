from django.contrib import admin

from django.utils.translation import ugettext as _

from models import *

class LocationAdmin(admin.ModelAdmin):
    list_display = ('title', )
    
    prepopulated_fields = {"slug": ("title",)}
    
admin.site.register(Location, LocationAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'event_date', 'start_time', 'location', 'publish')
    list_display_links = ('event_date', 'start_time', 'title')
    list_filter = ('event_date', 'publish', 'author', 'location')

    date_hierarchy = 'event_date'
    
    prepopulated_fields = {"slug": ("title",)}
    
    search_fields = ('title', 'location__title', 'author__username', 'author__first_name', 'author__last_name')        

    fieldsets =  ((None, {'fields': ['title', 'slug', 'event_date', 'start_time', 'end_time', 'location', 'description',]}),
                  (_('Advanced options'), {'classes' : ('collapse',),
                                           'fields'  : ('publish_date', 'publish', 'sites', 'author')}))
    
    # This is a dirty hack, this belongs inside of the model but defaults don't work on M2M
    def formfield_for_dbfield(self, db_field, **kwargs):
        """ Makes sure that by default all sites are selected. """
        if db_field.name == 'sites': # Check if it's the one you want
            kwargs.update({'initial': Site.objects.all()})
         
        return super(EventAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets_orig = super(EventAdmin, self).get_fieldsets(request, obj=None)

        # Hide author field if we don't have permissions
        if not request.user.has_perm('change_author'):
            for fieldset in fieldsets_orig:
                fieldset[1]['fields'].remove('author')        

        return fieldsets_orig

    def has_change_permission(self, request, obj=None):
        """ Make sure a user can only edit it's own entries. """

        if not obj:
            return True

        if obj.author == request.user:
            return True

        if request.user.has_perm('change_author'):
            return True

        return False
    # New code. Unfinished
    #     
    # def save_model(self, request, obj, form, change):
    #     if not request.user.has_perm('change_author'):
    #         obj.user = request.user
    #     
    #     super(EventAdmin, self).save_model(request, obj, form, change)

    # A little hack found in http://django.freelancernepal.com/topics/django-newforms-admin/
    def add_view(self, request, *args, **kwargs):
        if request.method == "POST":
            # If we DO NOT have change permissions, make sure we override the author to the current user
            if not request.user.has_perm('change_author'):
                postdict = request.POST.copy()
                postdict['author'] = request.user.id
                request.POST = postdict
      
        elif not request.GET.has_key('author'):
            # We are handling a GET, we default to current user
            getdict = request.GET.copy()
            getdict['author'] = request.user.id
            request.GET = getdict
                  
        return super(EventAdmin, self).add_view(request, *args, **kwargs)
     
    # there are hooks for this user stuff nowadays
    def change_view(self, request, *args, **kwargs):
        if request.method == "POST":
            # If we DO NOT have change permissions, make sure we override the author to the current user
            if not request.user.has_perm('change_author'):
                postdict = request.POST.copy()
                postdict['author'] = request.user.id
                request.POST = postdict

        return super(EventAdmin, self).change_view(request, *args, **kwargs)
    
admin.site.register(Event, EventAdmin)
