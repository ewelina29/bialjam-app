from django.conf.urls import url

from . import views

app_name = 'team'

urlpatterns = [
    url(r'^new/$', views.new, name='new'),
    url(r'details/(?P<id>[^/]+)/$', views.team_details, name='team_details'),
    url(r'my-team/$', views.my_team, name='my_team'),
    url(r'join-team/$', views.join_team, name='join_team'),
    url(r'request-user/$', views.request_user, name='request_user'),
    url(r'teams/', views.team_list, name='team_list')

]
