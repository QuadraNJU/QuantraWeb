from django.conf.urls import url

from users import views

urlpatterns = [
    url(r'^status', views.status),
    url(r'^login', views.login),
    url(r'^register', views.register),
    url(r'^logout', views.logout),
]
