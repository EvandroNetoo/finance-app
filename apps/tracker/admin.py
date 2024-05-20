from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as auth_UserAdmin
from tracker.models import Category, Transaction, User

admin.site.register(Transaction)
admin.site.register(Category)


@admin.register(User)
class UserAdmin(auth_UserAdmin):
    ...
