=============
django-agenda
=============

What is it?
===========
The django-agenda app is a generic
implementation of a web-based calendar
with events.

Status
======
Django-agenda is currently **not yet stable enough**
for production use *but* it can be fun to play around with.

Feautures
=========
*** I've managed to restore the code in just a few days! Woohoo! ***
Current
---------
- Full post-1.0 support, currently used on Django trunk.
- Kind admin interface with automatic author assignment (Django User).
- More elegant date_based generic view implementation. Finally you get all the info a decent archive will require. 
- Demo project with very basic templates.
- Event archive.
- Browseable calendar based on Python's calendar module.
- django.contrib.comments support
- django.contrib.sites support (with default value in admin)

Expected
--------
- vCard iCal/Google Calendar/Outlook export (lying around from an older project).
- Event feeds.
- Sitemaps.

Future
------
- User event suggestions: users can submit events to the app.

Requirements
============
All requirements are currently included in the "deps" directory.
- django-logging

License
=======
The django-agenda app is released 
under the GPL version 3.
