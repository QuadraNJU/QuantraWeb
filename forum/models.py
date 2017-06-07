# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Forum(models.Model):
    uid = models.IntegerField(null=False)
    time = models.DateTimeField(null=False)
    content = models.TextField(null=False)
    reply = models.IntegerField(null=False)