from django.conf.urls import url

from . import views

app_name = 'gallery'

urlpatterns = [
    url('albums', views.list_directories, name='list_directories'),
    url(r'album/(?P<id>[^/]+)/$', views.list_photos, name='list_photos'),

]
