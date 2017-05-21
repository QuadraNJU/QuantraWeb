# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=20, null=False, unique=True)
    password = models.CharField(max_length=70, null=False)
    nickname = models.CharField(max_length=20, null=False)
    email = models.EmailField(max_length=50, null=False)

    def __unicode__(self):
        return self.username
