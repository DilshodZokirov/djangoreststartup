from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from apps.users.forms import CustomUserCreationForm, CustomUserChangeForm
from apps.users.models import District, User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ('id', 'phone_number', 'is_staff', 'is_active', 'role', 'first_name', "is_director")
    list_filter = ('phone_number',)
    fieldsets = (
        (None, {'fields': (
            'phone_number', 'username', 'password', 'first_name', 'last_name', 'role', 'district', 'company')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', "is_director")}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password_one', 'password_two', 'phone_number', 'first_name', 'last_name', 'role',
                'company', 'district', "is_director"
            )
        }),
    )
    search_fields = ('phone_number',)
    ordering = ('phone_number',)


admin.site.register(User, CustomUserAdmin)


@admin.register(District)
class AdminDistrict(ModelAdmin):
    list_display = ['id', 'name']
