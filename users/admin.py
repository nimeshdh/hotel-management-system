from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    # Fields to display in the list view
    list_display = ('username', 'email', 'phone', 'role',
                    'is_active', 'is_staff', 'is_superuser')
    list_filter = ('role', 'is_active', 'is_staff')
    search_fields = ('username', 'email', 'phone')

    # Fields to edit in the user form
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name',
         'last_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff',
         'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for creating a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'role', 'phone', 'address'),
        }),
    )

    ordering = ('username',)


# Register the model with the admin site
admin.site.register(CustomUser, CustomUserAdmin)
