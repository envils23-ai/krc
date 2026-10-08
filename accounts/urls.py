from django.urls import path
from .views import SignUpView
from .views import CustomPasswordChangeView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),

    #Ссылка котора редериктит в Home после успешного изменения пароля.
    # Метод переопределен с generic на custom для messegess
    path('password_change/', CustomPasswordChangeView.as_view(), name='password_change'),
]