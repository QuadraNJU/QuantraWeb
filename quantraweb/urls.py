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
from trade import backtest_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TemplateView.as_view(template_name='container2.html')),
    url(r'^login$', TemplateView.as_view(template_name='login.html')),

    url(r'^api/stock/', include('stock.urls')),
    url(r'^api/user/', include('users.urls')),
    url(r'^api/trade/', include('trade.urls')),
    url(r'^api/forum/', include('forum.urls')),

    url(r'^ws/realtime_list', stock_views.realtime_list),
    url(r'^ws/realtime_price', stock_views.realtime_price),
    url(r'^ws/backtest', backtest_view.backtest),
]
