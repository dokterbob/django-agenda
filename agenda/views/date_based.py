from datetime import datetime

def process_context(context, extra_context):
    for key, value in extra_context.items():
        if callable(value):
            context[key] = value()
        else:
            context[key] = value

def get_object_context(queryset, year, month=None, day=None, num_objects=5, allow_empty=True):
    # Fetch relevant objects
    year = int(year)
    month = int(month)
    day = int(day)
    
    years = queryset.dates(date_field, 'year')
    if not years and not allow_empty:
        raise Http404, "No %s available" % model._meta.verbose_name

    object_context = { 'years' : years }
    queryset = queryset.filter(**{'%s__year' % date_field : year })
    
    object_context.update({'months' : queryset.dates(date_field, 'month'),
                           'year'   : year})

    if month:
        queryset = queryset.filter(**{'%s__month' % date_field : month })
        
        object_context.update({'days'  : queryset.dates(date_field, 'day'),
                               'month' : month })
    if day:
        queryset = queryset.filter(**{'%s__month' % date_field : day })
        
        object_context.update({'day'   : day })
    
    object_context.update({'objects' : queryset[:num_objects] })
                
    return object_context

def archive(request, queryset, date_field, 
            year, month=None, day=None, 
            template_name=None, template_object_list_name='objects', 
            num_objects=None, extra_context=None, allow_empty=None,
            mimetype=None, context_processors=None):

    # Get our model from the queryset
    model = queryset.model

    # Process parameters
    if not extra_context:
        extra_context = {}
    if not template_name:
        template_name = "%s/%s_archive.html" % (model._meta.app_label, model._meta.object_name.lower())

    object_context = { template_object_list_name : objects }

    # Get relevant context (objects and dates)
    object_context.update(get_object_context(year, month, day, num_objects, allow_empty))

    # Get a template, RequestContext and render
    t = template_loader.get_template(template_name)
    c = RequestContext(request, object_context, context_processors)
    
    process_context(c, extra_context)
    
    import logging
    logging.debug('Rendering with context: %s', c)
    
    return HttpResponse(t.render(c), mimetype=mimetype)

def index(request, queryset, date_field, 
          template_name=None, template_object_list_name='objects', 
          num_objects=5, extra_context=None,
          mimetype=None, context_processors=None):
    pass
    
def object_detail(request, queryset, date_field, 
                  year, month, slug, 
                  template_name=None, template_object_name='object',
                  extra_context=None,
                  mimetype=None, context_processors=None):
    pass