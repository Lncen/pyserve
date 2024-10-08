from django.db import models
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class PermissionGroupName(models.Model):
    """权限分组名称"""
    name = models.CharField(max_length=100)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True, related_name='content_type')

    class Meta:
        verbose_name = '权限分组名称'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PermissionGroup(models.Model):
    """权限分组"""
    permission_group = models.ForeignKey(PermissionGroupName, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)


    class Meta:
        verbose_name = '权限分组'
        verbose_name_plural = verbose_name

