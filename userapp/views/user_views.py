
from rest_framework import viewsets
from userapp.models.user import User
from userapp.serializers. user_serializer import UserSerializer
from common.baseviews.basegenericAPIView import BaseGenericAPIView

from ..serializers.user_serializer import UserGroupSerializer
from django.contrib.auth.models import Group


class UserViewSet(BaseGenericAPIView):
    """用户视图"""
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset()).filter(is_superuser=False)
        page = self.paginate_queryset(queryset)
        # 处理分页
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data).data


            group_all = Group.objects.all()
            group_all = UserGroupSerializer(group_all, many=True).data
            data['group_all'] = group_all
            return self.http_OK_response(message='成功', data=data)


