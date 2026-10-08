from django.urls import path
from .views import HomeView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('logout/', LogoutView.as_view(), name='logout'),
]