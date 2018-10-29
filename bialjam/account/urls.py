from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from . import views

app_name = 'account'
urlpatterns = [
    url(r'^login/$', auth_views.login, {'template_name': 'account/login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^details/$', views.update_profile, name='update_profile'),
    url(r'^users_list/$', views.users_list, name='users_list'),
    url(r'^user_details/(?P<pk>[^/d]+)/$', views.users_details, name='user_details'),

    url(r'^change-password/$', views.change_password, name='change_password'),
    url(r'^remove-user/$', views.remove_user, name="remove_user"),

    url(r'^password_reset/$',
        PasswordResetView.as_view(template_name='account/password_reset_form.html', email_template_name='account/password_reset_email.html', success_url='/accounts/password_reset/done/'),
        name='password_reset'),
    url(r'^password_reset/done/$',
        PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'),
        name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',
        success_url='/accounts/reset/done/'),
        name='password_reset_confirm'),
    url(r'^reset/done/$',
        PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'),
        name='password_reset_complete'),

]
