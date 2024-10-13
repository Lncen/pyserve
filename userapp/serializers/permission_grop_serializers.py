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


