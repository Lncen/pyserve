from rest_framework.response import Response
from rest_framework import status

"""
用于统一网页端返回信息
"""


def http_OK_response(message, data=None,code=0):
    """返回网页的信息"""
    return Response({
        'code': code,
        'message': message,
        'data': data
    }, status=status.HTTP_200_OK)


def http_BAD_response(message, data=None,code=1):
    """返回网页的信息"""
    return Response({
        'code': code,
        'message': message,
        'data': data
    }, status=status.HTTP_400_BAD_REQUEST)
