"""quantraweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from stock import views as stock_views


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='container2.html')),

    url(r'^api/society/', include('society.urls')),

    url(r'^api/stock/index', stock_views.get_index, name='stock_index'),
    url(r'^api/stock/market', stock_views.market),
    url(r'^api/stock/stock_list', stock_views.stock_list),
    url(r'^api/stock/stock', stock_views.stock),

    url(r'^ws/realtime_list', stock_views.realtime_list),
    url(r'^ws/realtime_price', stock_views.realtime_price),
]
