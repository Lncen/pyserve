from django.core.cache import cache
from rest_framework import permissions


class UserPermission(permissions.DjangoModelPermissions):
    """用户权限验证，规定用户必须拥有view（查看）权限 才可以拥有 删除 查看 新建的权限 """
    def __init__(self):
        # SAFE_METHODS 包括 GET, HEAD, OPTIONS
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

    def has_permission(self, request, view):
        # 调用父类的 has_permission 方法进行基本的身份验证和权限检查
        if not super().has_permission(request, view):
            return False

        # 获取查询集
        queryset = self._queryset(view)

        # 检查 GET 权限 只有拥有 GET 权限才可以进行其他操作
        perms = self.get_required_permissions('GET', queryset.model)
        cache_key = f'user_perms_{request.user.id}_{perms}'
        has_perms = cache.get(cache_key) # 获取缓存
        if has_perms is None:
            has_perms = request.user.has_perms(perms)
            cache.set(cache_key, has_perms, timeout=600)  # 缓存 10 分钟

        # 如果用户没有 GET 权限，拒绝所有请求
        if not has_perms:
            return False

        # 如果是其他请求方法，父类已经处理了权限检查
        return True



    def has_object_permission(self, request, view, obj):
        # 先检查用户是否已经通过身份验证
        if not request.user or not request.user.is_authenticated:
            return False
        # 检查用户是否有权限进行 GET 请求
        return super().has_object_permission(request, view, obj)
