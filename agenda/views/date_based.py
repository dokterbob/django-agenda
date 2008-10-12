from datetime import datetime, timedelta
from django.http import Http404, HttpResponse
from django.template import loader, RequestContext

import logging 


def process_context(context, extra_context):
    for key, value in extra_context.items():
        if callable(value):
            context[key] = value()
        else:
            context[key] = value

def get_object_context(queryset, date_field, year, month=None, day=None):
    # Fetch relevant objects
    objects = queryset.order_by('-%s' % date_field)
    
    object_context = { 'years' : objects.dates(date_field, 'year') }
    objects = objects.filter(**{'%s__year' % date_field : int(year) })
    
    object_context.update({'months'        : objects.dates(date_field, 'month'),
                           'year'          : int(year) })

    if month:
        objects = objects.filter(**{'%s__month' % date_field : int(month) })
        
        object_context.update({'days'  : objects.dates(date_field, 'day'),
                               'month' : int(month), })

    if day:
        objects = objects.filter(**{'%s__month' % date_field : int(day) })
        
        object_context.update({'day'   : int(day) })
    
    return objects, object_context

def archive(request, queryset, date_field, 
            year, month=None, day=None, 
            template_name=None, template_object_list_name='objects', template_loader=loader,
            num_objects=5, extra_context=None, allow_empty=True,
            mimetype=None, context_processors=None):

    # Get our model from the queryset
    model = queryset.model

    # Process parameters
    if not extra_context:
        extra_context = {}
    if not template_name:
        template_name = "%s/%s_archive.html" % (model._meta.app_label, model._meta.object_name.lower())

    # Get relevant context (objects and dates)
    objects, object_context = get_object_context(queryset, date_field, year, month, day)
    if not objects and not allow_empty:
        raise Http404, "No %s available" % model._meta.verbose_name
        
    object_context.update({ template_object_list_name : objects[:num_objects] })        

    # Get a template, RequestContext and render
    t = template_loader.get_template(template_name)
    c = RequestContext(request, object_context, context_processors)
    
    process_context(c, extra_context)
    
    logging.debug('Rendering with context: %s', c)
    
    return HttpResponse(t.render(c), mimetype=mimetype)

def index(request, queryset, date_field, 
          template_name=None, template_object_list_name='objects', template_loader=loader,
          num_objects=5, extra_context=None,
          mimetype=None, context_processors=None):
    pass
    
def object_detail(request, queryset, date_field, 
                  year, month, slug, 
                  template_name=None, template_object_name='object', template_loader=loader,
                  extra_context=None,
                  mimetype=None, context_processors=None):
    pass