
from rest_framework import serializers
from ..models import User
from django.contrib.auth.models import Group


class UserGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()
    balance = serializers.FloatField()  # 显式指定 balance 字段为浮点型
    class Meta:
        model = User
        #          ID    用户名       管理员      状态         积分       创建时间
        fields = ['id', 'username', 'is_staff','is_active','balance','date_joined','groups']
        # 只读
        read_only_fields = ['id', 'date_joined','username']
        extra_kwargs = {
            'date_joined': {
                'format': '%Y-%m-%d',
                'read_only': True  # 只读
            }  # 自定义日期时间格式
        }

    def get_groups(self, obj):
        """
        获取用户的组信息。

        :param obj: User 实例
        :return: 用户所属的组列表
        """
        return [group.id for group in obj.groups.all()]




