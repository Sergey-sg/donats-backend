from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserLoginForm
from .models import User, LinkToSocial, VolunteerInfo


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserLoginForm
    model = User
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (('Permissions', {'fields': ('is_staff', 'is_active')}),)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)


class LinkToSocialAdmin(admin.StackedInline):
    model = LinkToSocial


class VolunteerInfoAdmin(admin.ModelAdmin):
    list_display = ('public_name', 'first_name', 'last_name', 'user', 'active',)
    search_fields = ('public_name', 'first_name', 'last_name', 'user',)
    inlines = [LinkToSocialAdmin]
    list_filter = ['active']


admin.site.register(User, CustomUserAdmin)
admin.site.register(VolunteerInfo, VolunteerInfoAdmin)
