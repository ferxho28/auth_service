from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('first_name', 'last_name', 'email', 'is_verified', 'is_staff', 'created_at')
    list_filter = ('is_verified', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('-created_at',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('phone_number', 'is_verified')}),
    )
