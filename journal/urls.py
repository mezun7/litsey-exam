from django.conf.urls import patterns, include, url
from journal.views import LoginView

urlpatterns = patterns('journal.views',
                       # Examples:
                       # url(r'^$', 'tosterproject.views.home', name='home'),
                       # url(r'^blog/', include('blog.urls')),

                       url(r'^$', 'home', name='home'),
                       url(r'^login/$', LoginView.as_view(), name='login'),
                       url(r'^logout/$', 'log_out', name='logout'),
                       url(r'^class/(?P<class_id>\d+)/$', 'class_journal', name='class_journal'),
                       url(r'^test/$', 'raiting2', name='raiting2'),
                       url(r'^class/(?P<class_id>\d+)/master$', 'class_journal', name='my_class'),
                       url(r'^student/(?P<student_id>\d+)/$', 'student_profile', name='student'),
                       url(r'^raiting/(?P<parallel>\d+)/$', 'raiting', name='raiting'),
                       url(r'^inc/$', 'increase', name='inc'),
                       url(r'^phone/(?P<class_id>\d+)/$', 'get_phone_book', name='phone'),
                       url(r'^overall/$', 'get_overall', name='overall'),
                       url(r'^register/(?P<parallel>\d+)/$', 'students_list', name='list'),
                       url(r'^edit/(?P<stud_id>\d+)/$', 'student_edit', name='edit'),
                       url(r'^upload/$', 'upload_csv', name='upload'),
                       url(r'^delete/(?P<mark_id>\d+)/$', 'delete_mark', name='delete-mark'),
                       url(r'^print/$', 'print_raiting', name='print')
                       # url(r'^event/(?P<event_id>\d+)/edit/$', 'event_edit', name='event_edit')
                       )
