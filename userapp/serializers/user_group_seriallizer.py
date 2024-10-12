from django.contrib.auth.models import Group, Permission
from rest_framework import serializers
from .permission_serializer import PermissionSerializer
from ..management.commands.permission_type import permission_type
from ..models.permission_group import PermissionGroupName,PermissionGroup




class UserGroupSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name','permissions']

    def get_permissions(self, obj):
        # 获取组的所有权限
        permission_queryset = obj.permissions.all()
        detailed = self.context.get('detailed', False)

        # 只返回 id
        if detailed == 'id':
            return [perm.id for perm in permission_queryset]

        # 返回详细的权限信息
        serializer = PermissionSerializer(permission_queryset, many=True)
        return serializer.data


    def to_representation(self, instance):
        # 调用父类的方法获取初始表示
        representation = super().to_representation(instance)
        return representation


class PermissionGroupNameTreeWithPermissionsSerializer(serializers.ModelSerializer):
    """返回了所有分组"""
    children = serializers.SerializerMethodField()

    class Meta:
        model = PermissionGroupName
        fields = ['id', 'name', 'children']

    def get_children(self, obj):
        request = self.context.get('request')  # 获取请求中的用户对象
        if not request or not request.user.is_authenticated:
            return []  # 如果没有用户，返回空

        # 获取当前分组的子分组
        children_data = []
        child_groups = obj.children.all()

        # 获取当前用户的所有权限
        user_permissions = request.user.get_all_permissions()
        for child_group in child_groups:

            # 递归调用序列化器以处理子分组
            serialized_child = PermissionGroupNameTreeWithPermissionsSerializer(child_group, context=self.context).data
            # 获取与当前子分组关联的权限，并筛选出用户拥有的权限
            permission_qs = Permission.objects.filter(content_type_id=child_group.content_type_id)
            permissions_data = [
                {
                    'id': i.id,
                    'name': i.name
                } for i in permission_qs
                if f"{i.content_type.app_label}.{i.codename}" in user_permissions
            ]

            if permissions_data:
                serialized_child['children'] = permissions_data
            children_data.append(serialized_child)
        return children_data
