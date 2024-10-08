# userapp/tasks.py

from datetime import timedelta
from django.utils import timezone
from background_task import background
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken


@background(schedule=60 * 60 * 24)  # 每24小时运行一次
def cleanup_blacklisted_tokens():
    expiration_time = timezone.now() - timedelta(days=7)  # 例如，保留7天
    BlacklistedToken.objects.filter(blacklisted_at__lt=expiration_time).delete()
    print("已成功清理列入黑名单的令牌")