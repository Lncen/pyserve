
from rest_framework import viewsets
from rest_framework.fields import SerializerMethodField

from common.response import http_OK_response, http_BAD_response
from userapp.models.user import User
from userapp.serializers. user_serializer import UserSerializer
from common.baseviews.basegenericAPIView import BaseGenericAPIView

from ..serializers.user_group_seriallizer import UserGroupSerializer
from django.contrib.auth.models import Group, Permission
from userapp.models.permission_group import PermissionGroup, PermissionGroupName

from userapp.serializers.user_group_seriallizer import PermissionGroupNameTreeWithPermissionsSerializer


class UserGroupViewSet(BaseGenericAPIView):
    serializer_class = UserGroupSerializer
    queryset = Group.objects.all()  # 设置 queryset 属性

    def list(self, request, *args, **kwargs):
        page = self.paginate_queryset(self.queryset)
        # 处理分页
        serializer = self.get_serializer(page, many=True,context={'detailed': 'id'})
        response = self.get_paginated_response(serializer.data).data

        # 获取所有顶级分组
        top_level_groups = PermissionGroupName.objects.filter(parent=None)
        serializer = PermissionGroupNameTreeWithPermissionsSerializer(top_level_groups, many=True,                                                                 context={'request': request})
        response['groups']= [i for i in serializer.data if i['children'] ]

        return http_OK_response(data=response,message='成功')

    def create(self, request, *args, **kwargs):
        data =request.data
        if data['name']:
            goup = Group.objects.create(name=data['name'])
        return http_OK_response(message='成功')

# 更新 新建 删除 未完成

    def destroy(self, request, *args, **kwargs):
        try:
            group= Group.objects.get(id=kwargs['pk'])
            group.delete()
            return http_OK_response(message='成功')
        except:
            return http_OK_response(message='不存在的记录')

    def update(self, request, *args, **kwargs):
        data = request.data
        # 创建 Group 实例
        try:
            # 获取 Group 实例
            group = Group.objects.get(id=data['id'])

            # 获取当前权限
            current_permissions = group.permissions.all()

            # 获取需要保留的权限
            new_permissions = Permission.objects.filter(id__in=data['permissions'])

            # 计算需要删除的权限
            permissions_to_remove = [p for p in current_permissions if p.id not in data['permissions']]

            # 删除不需要的权限
            group.permissions.remove(*permissions_to_remove)

            # 添加新的权限
            group.permissions.add(*new_permissions)
            return http_OK_response(message=f"已添加到组的权限 '{group.name}' 成功")
        except Group.DoesNotExist:
            return http_BAD_response(message='未找到分组')
        except Permission.DoesNotExist:
            return http_BAD_response(message="未找到一个或多个权限.")
        except Exception as e:
            return http_BAD_response(message=f"发生错误: {str(e)}")
