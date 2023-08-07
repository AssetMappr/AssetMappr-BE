"""
This module maps the routes of API paths to respective views.

Author: Shashank Shekhar
"""
# from django.contrib import admin
# from rest_framework import routers
from django.urls import path
from assets import views

APP_NAME = "assets"
urlpatterns = [
    path("get_assets", views.AssetsView.as_view(), name="asset-list"),
]
