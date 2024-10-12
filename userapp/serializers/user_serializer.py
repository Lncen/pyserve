from django.contrib.auth.models import Group
from rest_framework import serializers
from ..models import User
from userapp.serializers.user_group_seriallizer import UserGroupSerializer


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField
    balance = serializers.FloatField(default=0.0000)  # 显式指定 balance 字段为浮点型
    # password = serializers.CharField(write_only=True)  # 添加密码字段，并设置为写入时只读
    class Meta:
        model = User
        #          ID    用户名       管理员      状态         积分       创建时间
        fields = ['id', 'username', 'password','is_staff','is_active','balance','date_joined','groups']
        # 只读
        read_only_fields = ['id', 'date_joined']
        extra_kwargs = {
            'date_joined': {
                'format': '%Y-%m-%d',
                'read_only': True  # 只读
            }, # 自定义日期时间格式
            'password': {'write_only': True, 'required': False}
        }
    def get_groups(self, obj):
        groups = UserGroupSerializer(obj.groups.all(), many=True).data
        return groups

    def create(self, validated_data):
        # 设置默认值，如果字段在请求中未提供
        # 创建用户时需要手动处理密码的哈希
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.balance = 0.0000
        user.is_active = True
        user.is_staff = False
        user.save()

        # 为用户设置默认分组
        default_group, created = Group.objects.get_or_create(name='普通用户')  # 替换 'default-group' 为你的默认分组名称
        user.groups.add(default_group)

        return user

