from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    """Кастомная админка для пользователей"""
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    list_per_page = 25


# Перерегистрируем модель User
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Настройка заголовков админки
admin.site.site_header = 'Fitness Integration Administration'
admin.site.site_title = 'Fitness Integration Admin'
admin.site.index_title = 'Dashboard'