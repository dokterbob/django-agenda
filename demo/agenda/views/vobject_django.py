from datetime import date, datetime, timedelta

from django.utils.html import strip_tags
from django.http import HttpResponse
from django.utils.tzinfo import FixedOffset

import vobject

def icalendar(request, queryset, date_field, ical_filename, 
              title_field='title', description_field='description',
              last_modified_field=None, location_field=None,
              start_time_field=None, end_time_field=None,
              num_objects=15, extra_context=None,
              mimetype=None, context_processors=None):
    
    now = datetime.now()      
    queryset = queryset.filter(event_date__gte=now - timedelta(days=1))
    
    cal = vobject.iCalendar()
    utc = vobject.icalendar.utc
    
    cal.add('method').value = 'PUBLISH'  # IE/Outlook needs this
    
    # Timezone code borrowed from 
    now = datetime.now()
    utcnow = datetime.utcnow()
    # Must always subtract smaller time from larger time here.
    if utcnow > now:
        sign = -1
        tzDifference = (utcnow - now)
    else:
        sign = 1
        tzDifference = (now - utcnow)
    
    # Round the timezone offset to the nearest half hour.
    tzOffsetMinutes = sign * ((tzDifference.seconds / 60 + 15) / 30) * 30
    tzOffset = timedelta(minutes=tzOffsetMinutes)
    
    #cal.add('vtimezone').value = FixedOffset(tzOffset)

    mytz = FixedOffset(tzOffset)
    
    for event in queryset:
        vevent = cal.add('vevent')

        vevent.add('summary').value = strip_tags(getattr(event, title_field))
        vevent.add('description').value = strip_tags(getattr(event, description_field))

        start_time = getattr(event, start_time_field, None)
        if start_time:
            start_date = datetime.combine(getattr(event, date_field), event.start_time)
            
            end_time = getattr(event, end_time_field, None)
            if end_time:
                end_date = datetime.combine(getattr(event, date_field), event.end_time)
                vevent.add('dtend').value = end_date.replace(tzinfo = mytz)
            
        else:
            start_date = getattr(event, date_field)
        
        
        # Date objects don't have tzinfo
        if isinstance(start_date, datetime):
            vevent.add('dtstart').value = start_date.replace(tzinfo = mytz)
        else:
            vevent.add('dtstart').value = start_date
        
        last_modified = getattr(event, last_modified_field, None)
        if last_modified:
            vevent.add('last-modified').value = last_modified.replace(tzinfo = mytz)
            
        location = getattr(event, location_field, None)
        if location:
            vevent.add('location').value = strip_tags(location)

    icalstream = cal.serialize()
    response = HttpResponse(icalstream, mimetype='text/calendar')
    response['Filename'] = ical_filename  # IE needs this
    response['Content-Disposition'] = 'attachment; filename=%s' % ical_filename

    return response
