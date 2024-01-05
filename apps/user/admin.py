from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserLoginForm
from .models import User, VolunteerInfo, LinkToSocial


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserLoginForm
    model = User
    list_display = list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('photo_profile', 'photo_alt',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),
    )
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
    extra = 0


@admin.register(VolunteerInfo)
class VolunteerInfoAdmin(admin.ModelAdmin):
    list_display = ('public_name', 'first_name', 'last_name', 'user', 'active',)
    inlines = [LinkToSocialAdmin]
    search_fields = ('public_name', 'first_name', 'last_name', 'user',)
    list_filter = ['active']
