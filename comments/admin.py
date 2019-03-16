from django.contrib import admin

# Register your models here.

from comments.models import User


class UsersAdmin(admin.ModelAdmin):
    list_display = ('uid', 'username', 'password', 'kind')


admin.site.register(User, UsersAdmin)