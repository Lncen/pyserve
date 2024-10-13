from rest_framework import viewsets, generics
from django.contrib.auth.models import Permission
from rest_framework.response import Response
from rest_framework.views import APIView

from common.baseviews.basegenericAPIView import BaseGenericAPIView
from userapp.models.permission_group import PermissionGroup, PermissionGroupName
from userapp.serializers.permission_grop_serializers import (PermissionGroupSerializer,
                                                             PermissionGroupNameSerializer
                                                             )
from userapp.serializers.user_group_seriallizer import PermissionGroupNameTreeWithPermissionsSerializer
from userapp.serializers.permission_serializer import PermissionSerializer
from common.response import http_OK_response,http_BAD_response



class PermissionGroupNameViewSet(BaseGenericAPIView):
    """权限分组名称"""
    queryset = PermissionGroupName.objects.all()
    serializer_class = PermissionGroupNameSerializer

class PermissionGroupViewSet(BaseGenericAPIView):
    """权限分组"""
    queryset = PermissionGroup.objects.all()
    serializer_class = PermissionGroupSerializer


class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    """权限"""
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    pagination_class = None  # 禁用分页
