from django.conf.urls import patterns, include, url

from django.contrib import admin
from litsey_exam import settings

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'litsey_exam.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^journal/', include('journal.urls', namespace='journal')),
    url(r'^media/(?P<path>.*)$','django.views.static.serve',
  		{'document_root' : settings.MEDIA_ROOT}
  		),
)
