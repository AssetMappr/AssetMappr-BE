"""
This module maps the routes of API paths to respective views.

Author: Shashank Shekhar
"""
# from django.contrib import admin
# from rest_framework import routers
from django.urls import path
from assets import views

# router.register(r'api/assets', views.AssetsView.as_view())
# router.register(r'api/assets/1', views.asset_detail, basename='api')
APP_NAME = "assets"
urlpatterns = [
    path("", views.AssetsView.as_view(), name="asset-list"),
]
