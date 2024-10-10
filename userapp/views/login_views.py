from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import generics, views

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from common.response import http_OK_response,http_BAD_response
from ..serializers.login_serializer import LoginSerializer

User = get_user_model()


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response_data = {
                    'token': response.data['access'],
                    'refresh': response.data['refresh']
            }
            # refresh_token = response.data['refresh']
            # print(response.data)
            # response.set_cookie(
            #     key='refresh_token',
            #     value=refresh_token,
            #     httponly=True,
            #     secure=False,  # 如果使用 HTTPS，启用此选项
            #     samesite='Strict'
            # )
            return http_OK_response(message='登录成功',data=response_data)
        else:
            # 在这里处理登录失败的情况
            return http_BAD_response(message='登陆失败')


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            # 调用父类的 post 方法进行 Token 刷新
            response = super().post(request, *args, **kwargs)

            # 如果 Token 刷新成功
            if response.status_code == status.HTTP_200_OK:
                response_data = {
                    'token': response.data['access'],
                }
                return http_OK_response(message='Token 刷新成功', data=response_data)
            else:
                return http_BAD_response(message='Token 刷新失败')

        except Exception as e:
            # 返回明确的错误响应
            return http_OK_response(code=11,message=str(e))


class LogoutView(views.APIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                raise Exception("在 Cookie 中找不到刷新令牌")
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({"code": 0, "message": "注销成功"}, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('refresh_token')
            return response
        except Exception as e:
            return Response({"code": 400, "message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(views.APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        print('5')
        # 获取当前登录的用户
        user = request.user
        # 检查用户是否已登录
        if user.is_authenticated:
            # 构建用户信息字典
            response = {
                'username': user.username,
                'roles':['admin']
                # 可以添加更多字段
            }
            return http_OK_response(message='成功',data=response)
        else:
            return Response({'error': 'User not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)