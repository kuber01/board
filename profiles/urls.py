from django.urls import path, include
from django.contrib.auth.views import auth_login

from .views import signup_view, account_confirmation

urlpatterns = [
    path('signup/', signup_view, name="signup"),
    path('confirmation/', account_confirmation, name="confirm"),
]
