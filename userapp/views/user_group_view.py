
from rest_framework import viewsets
from rest_framework.fields import SerializerMethodField

from common.response import http_OK_response
from userapp.models.user import User
from userapp.serializers. user_serializer import UserSerializer
from common.baseviews.basegenericAPIView import BaseGenericAPIView

from ..serializers.user_group_seriallizer import UserGroupSerializer
from django.contrib.auth.models import Group
from userapp.models.permission_group import PermissionGroup, PermissionGroupName

from userapp.serializers.user_group_seriallizer import PermissionGroupNameTreeWithPermissionsSerializer


class UserGroupViewSet(BaseGenericAPIView):
    serializer_class = PermissionGroupNameTreeWithPermissionsSerializer
    queryset = PermissionGroupName.objects.all()  # 设置 queryset 属性

    def list(self, request, *args, **kwargs):
        response = super(UserGroupViewSet, self).list(request, *args, **kwargs)
        # 获取所有顶级分组

        g = Group.objects.all()
        sg = UserGroupSerializer(g,many=True,context={'detailed': 'id'})
        response.data['data']['group_name']= sg.data

        results = response.data['data']['results']
        response.data['data']['results']= [i for i in results if i['children'] ]
        return response

# 更新 新建 删除 未完成

