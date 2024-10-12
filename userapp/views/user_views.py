
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
        response = super(UserViewSet, self).list(request, *args, **kwargs)
        group_all = Group.objects.all()
        group_all = UserGroupSerializer(group_all, many=True).data
        response.data['data']['group_all'] = group_all

        return response

