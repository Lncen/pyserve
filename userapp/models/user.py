from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """继承字内置user模型 添加了字段 balance"""
    # 添加自定义字段
    balance = models.DecimalField(max_digits=10, decimal_places=5, default=0.0000)

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username