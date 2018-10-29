from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'details/(?P<id>[^/]+)/$', views.post_detail, name='post_detail'),
    url(r'list/', views.post_list, name='post_list')
]
