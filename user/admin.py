from django.contrib import admin
from .models import RegisterUser, FollowPeople, Boards


# Register your models here.

class RegisterUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'country',
        'profile_image', 'is_superuser', 'last_login')


admin.site.register(RegisterUser, RegisterUserAdmin)


class FollowUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'follow_user')


admin.site.register(FollowPeople, FollowUserAdmin)


class BoardsAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'topic')


admin.site.register(Boards, BoardsAdmin)




