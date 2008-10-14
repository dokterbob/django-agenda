import logging

from django import template

register = template.Library()

@register.tag(name="previous")
def do_previous(parser, token):
    # previous in <list> from <object> as <previous_object> 
    bits = token.contents.split()
    if len(bits) != 7:
        raise template.TemplateSyntaxError, "%r takes six arguments" % bits[0]
        
    return PreviousNode(bits[2], bits[4], bits[6])

def get_previous(object_list, object_current):
    logging.debug('Finding previous of %s in %s' % (object_current, object_list))
    assert object_list.contains(object_current)

    index = object_list.index(object_current)    

    if index == 0:
        return None
    
    return object_list[index-1]
    
def get_next(object_list, object_current):
    logging.debug('Finding next of %s in %s' % (object_current, object_list))
    assert object_list.contains(object_current)

    index = object_list.index(object_current)    
    
    if index == len(object_list)-1:
        return None

    return object_list[index+1]
    
class PreviousNode(template.Node):
    def __init__(self, object_list, object_current, previous_name):
        self.object_list = template.Variable(object_list)
        self.object_current = template.Variable(object_current)
        self.previous_name = previous_name

    def render(self, context):
        logging.debug('blaat')
        logging.debug(self.object_list)

        object_list = self.object_list.resolve(context)
        object_current = self.object_current.resolve(context)
    
        from django.db.models.query import QuerySet
        logging.debug(object_list)
        if type(QuerySet()) == type(object_list):
            # This is efficient, but very experimental
            if len(object_list.query.order_by) == 1:
                if object_list.query.order_by[0][0] == '-':
                    date_field = object_list.query.order_by[0][1:]
                    prev_getter = getattr(object_current, 'get_previous_by_%s' % date_field, None)
                    if prev_getter:
                        object_previous = prev_getter()
                else:
                    date_field = object_list.query.order_by[0]
                    prev_getter = getattr(object_current, 'get_next_by_%s' % date_field, None)
                    if prev_getter:
                        object_previous = prev_getter()
                        
            previous_id = get_previous(object_list.values_list('id', flat=True), object_current.id)
            
            object_previous = object_list.get(id=previous_id)
        else:
            object_previous = get_previous(list(object_list), object_current)
            
        context[self.previous_name] = object_previous
        return ''