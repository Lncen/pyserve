from rest_framework import serializers
from ..models.permission_group import PermissionGroupName, PermissionGroup
from django.contrib.auth.models import Permission

class PermissionGroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionGroupName
        fields = ['id', 'name', 'parent']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name','content_type']

class PermissionGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionGroup
        fields = ['id', 'permission_group', 'permission']

class PermissionGroupNameTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = PermissionGroupName
        fields = ['id', 'name', 'parent', 'children']

    def get_children(self, obj):
        return PermissionGroupNameTreeSerializer(obj.children.all(), many=True).data

class PermissionGroupNameWithAncestorsSerializer(serializers.ModelSerializer):
    ancestors = serializers.SerializerMethodField()

    class Meta:
        model = PermissionGroupName
        fields = ['id', 'name', 'parent', 'ancestors']

    def get_ancestors(self, obj):
        return PermissionGroupNameSerializer(obj.get_ancestors(), many=True).data

class PermissionGroupNameWithDescendantsSerializer(serializers.ModelSerializer):
    descendants = serializers.SerializerMethodField()

    class Meta:
        model = PermissionGroupName
        fields = ['id', 'name', 'parent', 'descendants']

    def get_descendants(self, obj):
        return PermissionGroupNameSerializer(obj.get_descendants(), many=True).data

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
                    'permission': i.name
                } for i in permission_qs
                if f"{i.content_type.app_label}.{i.codename}" in user_permissions
            ]

            if permissions_data:
                serialized_child['children'] = permissions_data
            children_data.append(serialized_child)
        return children_data
