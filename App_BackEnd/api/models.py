from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, uid, nickname, password):
        if not uid:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        user = self.model(
            uid=self.normalize_email(uid),
            nickname=nickname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, uid, nickname, password):
        user = self.create_user(
            uid =uid,
            nickname=nickname,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    uid = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True, primary_key=True)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)
    password = models.CharField(default='', max_length=100, null=False, blank=False)
    birth = models.DateField(verbose_name="Birth")
    tot_concent_hour = models.IntegerField(verbose_name="Total Study Hour", default=0)
    SEX = (
        ('M', '남성(Man)'),
        ('W', '여성(Woman)'),
        ('N', '설정안함(None)'),
    )
    sex = models.CharField(max_length=1, choices=SEX)
    BADGE = (
        ('B', 'BRONZE'),
        ('S', 'SILVER'),
        ('G', 'GOLD'),
        ('P', 'PLATINUM'),
        ('D', 'DIAMOND'),
    )
    badge = models.CharField(max_length=2, choices=BADGE, default='B')

    # User 모델의 필수 field
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 nickname으로 설정
    USERNAME_FIELD = 'nickname'
    # 필수로 작성해야하는 field
    REQUIRED_FIELDS = ['uid', 'nickname', 'password']

    def __str__(self):
        return self.nickname