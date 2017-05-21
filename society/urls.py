from django.conf.urls import url

from society import views

app_name = 'society'
urlpatterns = [
    url(r'^$', views.login),
    url(r'^login/$', views.login, name='login'),
    url(r'^regist/$', views.regist, name='regist'),
    url(r'^logout/$', views.logout, name='logout'),
]
