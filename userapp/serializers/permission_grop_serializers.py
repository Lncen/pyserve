from django.contrib.auth.models import Permission
from rest_framework import serializers
from ..models.permission_group import PermissionGroupName, PermissionGroup

class PermissionGroupNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermissionGroupName
        fields = ['id', 'name', 'parent']

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
