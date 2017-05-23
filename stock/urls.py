from django.conf.urls import url

from stock import views

urlpatterns = [
    url(r'^index', views.get_index, name='stock_index'),
    url(r'^market', views.market),
    url(r'^stock_list', views.stock_list),
    url(r'^stock', views.stock),
]
