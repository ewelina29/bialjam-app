from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^jury$', views.vip_jury, name='vip_jury'),
    url(r'details/(?P<id>[^/]+)/$', views.vip_details, name='vip_details'),

]
