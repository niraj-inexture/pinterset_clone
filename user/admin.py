from django.contrib import admin
from .models import RegisterUser


# Register your models here.

class RegisterUserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'is_active', 'gender', 'country',
        'profile_image', 'is_superuser', 'last_login')


admin.site.register(RegisterUser, RegisterUserAdmin)




