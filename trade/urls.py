from django.conf.urls import url

from trade import stockpool_view, strategy_view

urlpatterns = [
    url(r'^createPool', stockpool_view.createPool),
    url(r'^readPool', stockpool_view.readPool),
    url(r'^updatePoolById', stockpool_view.updatePoolById),
    url(r'^deletePoolById', stockpool_view.deletePoolById),

    url(r'^createStrategy', strategy_view.createStrategy),
    url(r'^readStrategy', strategy_view.readStrategy),
    url(r'^updateStrategyById', strategy_view.updateStrategyById),
    url(r'^deleteStrategyById', strategy_view.deleteStrategyById),
]
