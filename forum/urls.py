from django.conf.urls import url

from forum import views

urlpatterns = [
    url(r'^getlist$', views.get_list),
    url(r'^get$', views.get_thread),
    url(r'^new$', views.new_thread),
    url(r'^delete$', views.delete_thread),
]
