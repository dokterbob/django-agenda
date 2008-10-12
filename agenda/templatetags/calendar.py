from django import template

from calendar import calendar
from datetime import datetime

import re

register = template.Library()

@register.tag(name="get_calendar")
def do_calendar(parser, token):
    syntax_help = "syntax should be get_calendar for <month> <year> as <var_name>"
    # This version uses a regular expression to parse tag contents.
    try:
        # Splitting by None == splitting by spaces.
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments, %s" % (token.contents.split()[0], syntax_help)
    m = re.search(r'for ([0-9]{1,2}) ([0-9]{4}) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%r tag had invalid arguments, %s" % (tag_name, syntax_help)
    year, month, var_name = m.groups()
    
    return GetCalendarNode(int(year), int(month), var_name)

class GetCalendarNode(template.Node):
    def __init__(self, year, month, var_name):
        self.year = year
        self.month = month
        self.var_name = var_name
        
    def render(self, context):
        mycal = calendar()
        context[self.var_name] = mycal.monthdatescalendar(self.year, self.month)
        
        return ''
        