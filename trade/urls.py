from django.conf.urls import url

from trade import stockpool_view, strategy_view

urlpatterns = [
    url(r'^pool/get$', stockpool_view.readPool),
    url(r'^pool/getbyid$', stockpool_view.getPoolById),
    url(r'^pool/update$', stockpool_view.updatePool),
    url(r'^pool/delete$', stockpool_view.deletePoolById),

    url(r'^strategy/getlist$', strategy_view.get_list),
    url(r'^strategy/getdetail$', strategy_view.get_detail),
    url(r'^strategy/update$', strategy_view.update),
    url(r'^strategy/delete$', strategy_view.delete),
]
