import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'litsey_exam.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())