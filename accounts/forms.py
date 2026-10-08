from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AdminUserCreationForm
from Home.models import CustomUser

# Создание пользователя с сайта
class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields

# Создание пользователя с админки
class CustomUserAdminCreationForm(AdminUserCreationForm):  # для админки
    class Meta(AdminUserCreationForm.Meta):
        model = CustomUser
        fields = AdminUserCreationForm.Meta.fields

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = UserChangeForm.Meta.fields

