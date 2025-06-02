from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Goods

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_blacklisted', 'is_staff')
    list_filter = ('is_blacklisted', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('is_blacklisted',)}),
    )

admin.site.register(User, CustomUserAdmin)
admin.site.register(Goods)
