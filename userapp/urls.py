from django.urls import path, include
from rest_framework.routers import DefaultRouter

from userapp.views.login_views import LoginView,CustomTokenRefreshView,UserInfoView,LogoutView
from userapp.views.permission_groups_view import PermissionGroupNameTreeWithPermissionsView, PermissionGroupViewSet, PermissionGroupNameViewSet, PermissionViewSet
from userapp.views.user_views import UserViewSet

router = DefaultRouter()
router.register(r'permission-groups', PermissionGroupViewSet)
router.register(r'permissions-group_name', PermissionGroupNameViewSet)
router.register(r'permissions', PermissionViewSet)
router.register(r'users', UserViewSet)




urlpatterns = [
    path('', include(router.urls)),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('info/',UserInfoView.as_view(),name='user_info'),
    path('psnt/',PermissionGroupNameTreeWithPermissionsView.as_view(),name='psnt')

]

