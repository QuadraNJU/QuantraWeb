# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class StockPool(models.Model):
    uid = models.IntegerField(null=False)
    name = models.CharField(max_length=50, null=False)
    stock_list = models.TextField(null=False)


class Strategy(models.Model):
    uid = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)
    name = models.CharField(max_length=50, null=False)
    description = models.TextField(null=False)
    code = models.TextField(null=False)
    parameters = models.TextField(null=False)
    is_public = models.BooleanField(null=False)


class BacktestResult(models.Model):
    uid = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)
    strategy = models.IntegerField(null=False)
    parameter = models.TextField(null=False)
    result = models.TextField(null=False)


class SimAccount(models.Model):
    uid = models.IntegerField(null=False)
    cash = models.FloatField(null=False, default=100000)


class Position(models.Model):
    uid = models.IntegerField(null=False)
    code = models.IntegerField(null=False)
    amount = models.IntegerField(null=False, default=0)
    buy_price = models.FloatField(null=False)
