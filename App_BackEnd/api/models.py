from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models
import uuid

# Create your models here.


class Account(models.Model):

    uid = models.EmailField(verbose_name="ID", max_length=60, unique=True, blank=False, primary_key= True, default='')
    username = models.CharField(verbose_name="NickName", max_length=30, blank=False,null=True )
    password = models.CharField(verbose_name="PassWord", max_length=30, blank=False, null=True )
    birth = models.DateField(verbose_name="Birth", null=True )
    tot_concent_hour = models.IntegerField(verbose_name="Total Study Hour", default=0,null=True )
    SEX = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
        ('N', '설정안함(None)'),
    )
    sex = models.CharField(max_length=1, choices=SEX,null=True )
    BADGE = (
        ('B', 'BRONZE'),
        ('S', 'SILVER'),
        ('G', 'GOLD'),
        ('P', 'PLATINUM'),
        ('D', 'DIAMOND'),
    )
    badge = models.CharField(max_length=2, choices=BADGE, default='B', null=True )


    def __str__(self):
        return self.user.username

