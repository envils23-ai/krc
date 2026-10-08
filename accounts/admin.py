from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserAdminCreationForm, CustomUserChangeForm
from Home.models import CustomUser

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserAdminCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = [
        'username',
    ]
    # fieldsets = UserAdmin.fieldsets
    # add_fieldsets = UserAdmin.add_fieldsets

admin.site.register(CustomUser, CustomUserAdmin)
