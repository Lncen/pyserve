# 依赖
- 将整个python环境下的库导出到requirements.txt
```shell
pip freeze > requirements.txt
```

```shell
pip install djangorestframework-simplejwt
pip install django-cors-headers
pip install mysqlclient
pip install django-celery-beat celery
```
- 自动任务
- django-background-tasks 是一个 Django 应用，可以用来在后台运行任务。
- 配置
配置 
- settings.py： 在 INSTALLED_APPS 中添加 background_tasks：
- BACKGROUND_TASK_RUN_ASYNC 以异步运行任务：
```shell
INSTALLED_APPS = [    
    'background_tasks',
]
BACKGROUND_TASK_RUN_ASYNC = True  # 异步运行任务
MAX_ATTEMPTS = 10  # 最大重试次数
MAX_RUN_TIME = 3600  # 单个任务的最大运行时间（秒）
```

---
# 刷新令牌过去返回的
- {
    "detail": "令牌无效或已过期",
    "code": "token_not_valid"
}

---
# 数据库
## 迁徙
-删除现有的迁徙文件
```shell
rm userapp/migrations/0001_initial.py
```
- 重新生成uerapp 的迁徙文件
```shell
python manage.py makemigrations userapp
```
- 应用迁徙
```shell
python manage.py migrate
```

# 要求
需要运行定时任务程序
```shell
python manage.py process_tasks
```

# CURD
create 方法：
创建一个新的权限分组名称。
返回自定义的响应，包含用户名和角色信息。

update 方法：
更新一个权限分组名称。
返回自定义的响应，包含用户名和角色信息。

partial_update 方法：
部分更新一个权限分组名称。
调用 update 方法，传递 partial=True。

destroy 方法：
删除一个权限分组名称。
返回自定义的响应，包含用户名和角色信息。

retrieve 方法：
查询一个特定的权限分组名称。
返回自定义的响应，包含用户名、角色信息和序列化后的数据。

list 方法：
获取权限分组名称的列表。
如果启用了分页，返回分页后的数据。
如果没有启用分页，返回所有数据。