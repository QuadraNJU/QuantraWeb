from django.conf.urls import url

from trade import stockpool_view, strategy_view, backtest_view, simulate_view

urlpatterns = [
    url(r'^pool/get$', stockpool_view.readPool),
    url(r'^pool/getbyid$', stockpool_view.getPoolById),
    url(r'^pool/update$', stockpool_view.updatePool),
    url(r'^pool/delete$', stockpool_view.deletePoolById),

    url(r'^strategy/getlist$', strategy_view.get_list),
    url(r'^strategy/getdetail$', strategy_view.get_detail),
    url(r'^strategy/getpublic$', strategy_view.get_public_list),
    url(r'^strategy/update$', strategy_view.update),
    url(r'^strategy/delete$', strategy_view.delete),
    url(r'^strategy/clone$', strategy_view.clone_public),

    url(r'^backtest/gethistorylist$', backtest_view.get_history_list),
    url(r'^backtest/gethistory$', backtest_view.get_history),

    url(r'^simulate/init$', simulate_view.init_account),
    url(r'^simulate/getlist$', simulate_view.list),
    url(r'^simulate/trade$', simulate_view.trade),
    url(r'^simulate/getprice$', simulate_view.latest_price),
]
