# coding=utf-8
from django.http import JsonResponse

from stock.data import qtshare
from trade.models import SimAccount, Position


def init_account(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        amount = int(request.GET.get('amount', 100000))
        account = SimAccount.objects.filter(uid=uid)
        if account:
            account = account[0]
        else:
            account = SimAccount(uid=uid)
        account.amount = amount
        try:
            account.save()
            pos = Position.objects.filter(uid=uid)
            if pos:
                pos.delete()
            return JsonResponse({'ok': True})
        except:
            return JsonResponse({'ok': False, 'msg': '服务器异常'})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def list(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        account = SimAccount.objects.filter(uid=uid)
        if account:
            account = account[0]
        else:
            account = SimAccount(uid=uid)
            account.save()
        pos = Position.objects.filter(uid=uid)
        prices = qtshare.today_list()
        assets = account.cash
        positions = []
        for po in pos:
            price = prices[prices['code'] == po.code].iloc[0]['price']
            assets += po.amount * price
            positions.append({'code': po.code, 'amount': po.amount, 'buy_price': po.buy_price, 'price': price})
        return JsonResponse({'ok': True, 'cash': account.cash, 'assets': assets, 'positions': positions})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def trade(request):
    if 'uid' in request.session:
        uid = request.session['uid']
        account = SimAccount.objects.filter(uid=uid)
        if account:
            account = account[0]
        else:
            return JsonResponse({'ok': False, 'msg': '模拟交易账户不存在，请先创建账户'})
        code = int(request.POST.get('code', 0))
        amount = int(request.POST.get('amount', 0))
        prices = qtshare.today_list()
        price = prices[prices['code'] == code].iloc[0]['price']
        if amount > 0:  # 买入
            account.cash = account.cash - amount * price
            if account.cash < 0:
                return JsonResponse({'ok': False, 'msg': '买入失败：账户资金不足'})
            account.save()
            pos = Position.objects.filter(uid=uid, code=code)
            if pos:
                pos = pos[0]
                pos.buy_price = (pos.buy_price * pos.amount + price * amount) / (pos.amount + amount)
                pos.amount += amount
            else:
                pos = Position(uid=uid, code=code, amount=amount, buy_price=price)
            pos.save()
        else:  # 卖出
            pos = Position.objects.filter(uid=uid, code=code)
            if not pos:
                return JsonResponse({'ok': False, 'msg': '卖出失败：持仓股数不足'})
            pos = pos[0]
            pos.amount += amount
            if pos.amount < 0:
                return JsonResponse({'ok': False, 'msg': '卖出失败：持仓股数不足'})
            elif pos.amount == 0:
                pos.delete()
            else:
                pos.save()
            account.cash = account.cash - amount * price
            account.save()
        return JsonResponse({'ok': True})
    else:
        return JsonResponse({'ok': False, 'msg': '请登录后重试'})


def latest_price(request):
    code = int(request.GET.get('code', 0))
    prices = qtshare.today_list()
    price = prices[prices['code'] == code]
    if len(price) > 0:
        price = price.iloc[0]['price']
        return JsonResponse({'ok': True, 'price': price})
    else:
        return JsonResponse({'ok': False, 'msg': '获取价格失败'})
