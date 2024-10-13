from functools import update_wrapper
from pickle import PROTO

from celery import group
from celery.app.builtins import add_group_task
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from rest_framework.decorators import permission_classes

from userapp.models.permission_group import PermissionGroupName
from userapp.serializers.permission_grop_serializers import PermissionGroupNameSerializer
from userapp.serializers.permission_serializer import PermissionSerializer


# 翻译字典
zh_hans = {
    '用户管理': [None,'用户管理'],
    '系统管理': [None,'系统管理'],
    '权限管理': [None,'权限管理'],
    '商品管理': [None,'商品管理'],
    'log entry': ['权限管理','日志'],
    'permission': ['权限管理','权限'],
    'group': ['用户管理','用户分组'],
    'content type': ['权限管理','模型分类'],
    'session': ['权限管理','session'],
    'completed task': ['权限管理','已完成任务'],
    'task': ['权限管理','任务'],
    'blacklisted token': ['权限管理','令牌黑名单'],
    'outstanding token': ['权限管理','未过期令牌'],
    '用户': ['用户管理','用户'],
    '权限分组名称':['权限管理','权限分组名称'],
    '权限分组':['权限管理','权限分组']

}

permission_type={
    'delete':'删除',
    'view':'查看',
    'add':'新建',
    'change':'更新'
}



# 定义一个简单的权限序列化器
class PermissionWithTranslationSerializer:
    def set_permission(self):
        p = Permission.objects.all()
        for i in p:
            # 更新权限表
            names = i.name.split(' ')
            name = ' '.join(names[2:])
            if name in zh_hans:

                per = permission_type[names[1]] + zh_hans[name][1]
                i.name = per
                i.save()

        # 遍历所有 Permission 对象
        for i in p:
            group_name = i.name[2:]  # 假设 group_name 是从权限名称中提取的

            for k, v in zh_hans.items():
                if group_name == v[1]:

                    parent_group = None if v[0] is None else PermissionGroupName.objects.get(name=v[0])
                    content_type = i.content_type

                    defaults = {
                        'name': v[1],
                        'content_type': content_type,
                        'parent': parent_group
                    }

                    a, created = PermissionGroupName.objects.update_or_create(
                        name=v[1],
                        defaults=defaults
                    )
                    break  # 找到匹配项后退出内层循

        print('权限分组更新完成')



    def run(self):
        self.set_permission()
        # print(self.undata())


class Command(BaseCommand):
    # 使用命令 python manage.py permission_type
    help = '打印所有权限及其翻译名称 和权限分组'

    def handle(self, *args, **options):
        print('权限分组更新完成')
        # 获取所有 Permission 对象
        PermissionWithTranslationSerializer().run()

