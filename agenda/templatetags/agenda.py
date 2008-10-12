from django import template

from calendar import Calendar
import datetime

import re

register = template.Library()

import logging 

@register.tag(name="get_calendar")
def do_calendar(parser, token):
    syntax_help = "syntax should be \"get_calendar for <month> <year> as <var_name>\""
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments, %s" % (token.contents.split()[0], syntax_help)
    m = re.search(r'for (.*?) (.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments, %s" % (tag_name, syntax_help)
    
    return GetCalendarNode(*m.groups())

class GetCalendarNode(template.Node):
    def __init__(self, month, year, var_name):
        self.year = template.Variable(year)
        self.month = template.Variable(month)
        self.var_name = var_name
        
    def render(self, context):
        mycal = Calendar()
        context[self.var_name] = mycal.monthdatescalendar(int(self.year.resolve(context)), int(self.month.resolve(context)))
        
        return ''
        
class IfInNode(template.Node):
    '''
    Like {% if %} but checks for the first value being in the second value (if a list). Does not work if the second value is not a list.
    '''
    def __init__(self, var1, var2, nodelist_true, nodelist_false, negate):
        self.var1, self.var2 = var1, var2
        self.nodelist_true, self.nodelist_false = nodelist_true, nodelist_false
        self.negate = negate

    def __str__(self):
        return "<IfNode>"

    def render(self, context):
        val1 = template.resolve_variable(self.var1, context)
        val2 = template.resolve_variable(self.var2, context)
        try:
            val2 = list(val2)
            if (self.negate and datetime.datetime(*val1.timetuple()[:3]) not in val2) or (not self.negate and datetime.datetime(*val1.timetuple()[:3]) in val2):
                return self.nodelist_true.render(context)
            return self.nodelist_false.render(context)
        except TypeError:
            return self.nodelist_false.render(context)

def ifin(parser, token, negate):
    bits = token.contents.split()
    if len(bits) != 3:
        raise template.TemplateSyntaxError, "%r takes two arguments" % bits[0]
    end_tag = 'end' + bits[0]
    nodelist_true = parser.parse(('else', end_tag))
    token = parser.next_token()
    if token.contents == 'else':
        nodelist_false = parser.parse((end_tag,))
        parser.delete_first_token()
    else: nodelist_false = template.NodeList()
    return IfInNode(bits[1], bits[2], nodelist_true, nodelist_false, negate)

register.tag('ifdayin', lambda parser, token: ifin(parser, token, False))

        