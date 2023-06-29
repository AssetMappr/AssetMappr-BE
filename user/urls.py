from django.urls import path
from . import views

APP_NAME = "user"
urlpatterns = [
    path("signup", views.SignupView.as_view(), name="signup"),
    path("login", views.LoginView.as_view(), name="login"),
]
