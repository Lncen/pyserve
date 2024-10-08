from django.contrib import admin

# Register your models here.


from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from userapp.models.user import User

admin.site.register(User, UserAdmin)
# admin.site.register(Group, GroupAdmin)