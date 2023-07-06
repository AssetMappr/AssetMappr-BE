"""Urls file"""
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

APP_NAME = "user"
urlpatterns = [
    path("signup", views.SignupView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
    path("refresh-token/", TokenRefreshView.as_view(), name="refresh_token"),
]
