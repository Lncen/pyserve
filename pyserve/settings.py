"""
pyserve 项目的 Django 设置。

由 'django-admin startproject' 使用 Django 5.1.1 生成。

有关此文件的更多信息，请参阅
https://docs.djangoproject.com/en/5.1/topics/settings/

有关设置及其值的完整列表，请参阅
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

from datetime import timedelta

# 在项目内构建路径，如下所示：BASE_DIR / 'subdir'。
BASE_DIR = Path(__file__).resolve().parent.parent


# 快速启动开发设置 - 不适合生产
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# 安全警告：对生产中使用的密钥保密！
SECRET_KEY = 'django-insecure-sy=g0t@g1oij2@l8t3-ykubupxjm$2=jdy!&h4#xb!=up))#e4'

# 安全警告：请勿在生产环境中开启调试的情况下运行！
DEBUG = True

ALLOWED_HOSTS = []



REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        #  权限认证
        'common.permissions.user_permission.UserPermission'  # 自定义的权限类
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 身份认证
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',  # 在rest_framework后台保持登录状态
    ],

    # 分页
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,  # 设置默认每页大小为10
}

SIMPLE_JWT = {
    # 访问令牌的有效时间
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # 访问令牌在 5 分钟后过期

    # 刷新令牌的有效时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # 刷新令牌在 1 天后过期

    # 是否在每次使用刷新令牌时生成新的刷新令牌
    'ROTATE_REFRESH_TOKENS': True,  # 不旋转刷新令牌

    # 是否在旋转刷新令牌后将旧的刷新令牌加入黑名单
    'BLACKLIST_AFTER_ROTATION': True,  # 不将旧的刷新令牌加入黑名单

    # 是否在每次成功认证时更新用户的最后登录时间
    'UPDATE_LAST_LOGIN': False,  # 不更新用户的最后登录时间

    # 签名算法
    'ALGORITHM': 'HS256',  # 使用 HMAC 算法

    # 签名密钥
    'SIGNING_KEY': SECRET_KEY,  # 使用 Django 的 SECRET_KEY 作为签名密钥

    # 验证密钥
    'VERIFYING_KEY': None,  # 不指定验证密钥，使用签名密钥

    # 受众
    'AUDIENCE': None,  # 不指定受众

    # 发行人
    'ISSUER': None,  # 不指定发行人

    # JWK URL
    'JWK_URL': None,  # 不指定 JWK URL

    # 时间容差
    'LEEWAY': 0,  # 不设置时间容差

    # 认证头类型
    'AUTH_HEADER_TYPES': ('Bearer',),  # 认证头类型为 Bearer

    # 认证头名称
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # 认证头名称为 HTTP_AUTHORIZATION

    # 用户 ID 字段
    'USER_ID_FIELD': 'id',  # 用户 ID 字段为 id

    # 用户 ID 声明
    'USER_ID_CLAIM': 'user_id',  # 用户 ID 声明为 user_id

    # 用户认证规则
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',  # 使用默认的用户认证规则

    # 认证令牌类
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # 认证令牌类为 AccessToken

    # 令牌类型声明
    'TOKEN_TYPE_CLAIM': 'token_type',  # 令牌类型声明为 token_type

    # 令牌用户类
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',  # 令牌用户类为 TokenUser

    # JWT ID 声明
    'JTI_CLAIM': 'jti',  # JWT ID 声明为 jti

    # 滑动令牌刷新过期声明
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',  # 滑动令牌刷新过期声明为 refresh_exp

    # 滑动令牌有效时间
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),  # 滑动令牌在 5 分钟后过期

    # 滑动令牌刷新有效时间
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),  # 滑动令牌刷新在 1 天后过期
}

# 允许来自特定域的请求
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:3333/',
#     'http://192.168.2.2:3333/'
# ]


# 或者允许所有域
CORS_ALLOW_ALL_ORIGINS = True



### 以上自定义 设置#########

# 应用程序定义
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'background_task',

    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # 跨域请求
    'corsheaders',
    'userapp',


]

# django_background_tasks 设置
BACKGROUND_TASK_RUN_ASYNC = True  # 异步运行任务
BACKGROUND_TASK_QUEUE_WAITING_LIST_MAX_LENGTH = 1000  # 队列最大长度

# 中间件
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 跨域
    'corsheaders.middleware.CorsMiddleware',
]

# 用户模型
AUTH_USER_MODEL = 'userapp.User'
# 根路由
ROOT_URLCONF = 'pyserve.urls'

# 模板
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 应用程序
WSGI_APPLICATION = 'pyserve.wsgi.application'

# 数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pyserve',
        'USER': 'root',  # 数据库名字用户名
        'PASSWORD': '0000....',  # 数据库密码
        'HOST': '127.0.0.1',
        'PORT': '3306',  # 端口
        'OPTIONS': {'charset': 'utf8mb4'},  # 打开数据库 编码格式 ——解决4字节表情无法储存问题
    }
}


# 密码验证
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# 国际化
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True


# 静态文件（CSS、JavaScript、图像）
STATIC_URL = 'static/'

# 默认主键字段类型
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

