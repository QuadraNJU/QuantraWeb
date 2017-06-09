from django.conf.urls import url

from forum import views

urlpatterns = [
    url(r'^getlist$', views.get_list),
]
