from django.apps import AppConfig
from django.core.exceptions import AppRegistryNotReady

# from .tasks.cleanup_blacklisted_tokens import cleanup_blacklisted_tokens


class UserappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userapp'
    #
    # def ready(self):
    #     try:
    #         # 调用 cleanup_blacklisted_tokens 函数
    #         cleanup_blacklisted_tokens(repeat=60 * 60 * 24)  # 每24小时重复一次
    #     except AppRegistryNotReady:
    #         import traceback
    #         traceback.print_exc()
    #         print("应用程序尚未加载。延迟任务初始化。")