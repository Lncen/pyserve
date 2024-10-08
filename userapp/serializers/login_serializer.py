from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class LoginSerializer(TokenObtainPairSerializer):
    """用户登录获取token"""
    def validate(self, attrs):
        # 获取用户名和密码
        username = attrs.get('username')
        password = attrs.get('password')
        # 验证用户
        user = authenticate(request=self.context.get('request'), username=username, password=password)
        if not user:
            # 返回自定义错误消息
            data = {
                'code': 1,
                'message': '用户名或密码错误',
                'data': {}
            }
            raise serializers.ValidationError(data)

        # 生成 token
        data = super().validate(attrs)
        return data
