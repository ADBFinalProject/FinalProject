from django.conf.urls import url
from . import views

app_name = 'website'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.log_in, name='login'),
    url(r'^auth/$', views.auth_view, name='auth_view'),
    url(r'^signup/$', views.UserFormView.as_view(), name='signup'),
    url(r'^profile/home/$', views.home, name='home'),
    url(r'^profile/home/logout/$', views.logout, name='logout'),
]
