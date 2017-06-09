# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Thread(models.Model):
    uid = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)
    title = models.TextField(null=False)
    content = models.TextField(null=False)
    tag = models.CharField(null=False, max_length=50, default='')
    reply = models.IntegerField(null=False, default=0)
