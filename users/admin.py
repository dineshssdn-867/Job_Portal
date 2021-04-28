from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account, Profile, Invite


class MyAdminAccounts(UserAdmin):
    model = Account
    list_display = ('email', 'first_name', 'last_name', 'is_employee', 'is_employer')
    list_filter = ('email', 'first_name', 'last_name', 'is_employee', 'is_employer')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email', 'first_name')
    readonly_fields = ['date_joined']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2', 'is_employee', 'is_employer', 'is_active')
        }),
    )

    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_employee', 'is_employer')})
    )


admin.site.register(Account, MyAdminAccounts)
admin.site.register(Profile)
admin.site.register(Invite)

