import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'litsey_exam.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
