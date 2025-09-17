from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'avatar'),
        }),
    )

    fieldsets = UserAdmin.fieldsets + (
        ('Avatar', {'fields': ('avatar',)}),
    )


admin.site.register(CustomUser, CustomUserAdmin)