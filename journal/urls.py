from django.conf.urls import patterns, include, url
from journal.views import LoginView


urlpatterns = patterns('journal.views',
    # Examples:
    # url(r'^$', 'tosterproject.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$','home', name='home'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', 'log_out', name='logout'),
    url(r'^class/(?P<class_id>\d+)/$', 'class_journal', name='class_journal'),
    url(r'^test/$', 'raiting2', name='raiting2'),
    url(r'^class/(?P<class_id>\d+)/master$', 'class_journal', name='my_class'),
    url(r'^student/(?P<student_id>\d+)/$', 'student_profile', name='student'),
    url(r'^raiting/$', 'raiting', name='raiting'),
    url(r'^inc/$', 'increase', name='inc')
    #url(r'^event/(?P<event_id>\d+)/edit/$', 'event_edit', name='event_edit')
)
