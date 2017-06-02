from django.conf.urls import url

from trade import stockpool_view, strategy_view

urlpatterns = [
    url(r'^pool/create', stockpool_view.createPool),
    url(r'^pool/get', stockpool_view.readPool),
    url(r'^pool/update', stockpool_view.updatePoolById),
    url(r'^pool/delete', stockpool_view.deletePoolById),

    url(r'^createStrategy', strategy_view.createStrategy),
    url(r'^readStrategy', strategy_view.readStrategy),
    url(r'^updateStrategyById', strategy_view.updateStrategyById),
    url(r'^deleteStrategyById', strategy_view.deleteStrategyById),
]
