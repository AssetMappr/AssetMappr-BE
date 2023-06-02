from django.contrib import admin
from rest_framework import routers
from django.urls import path, re_path, include
from assets import views

# router.register(r'api/assets', views.AssetsView.as_view())
# router.register(r'api/assets/1', views.asset_detail, basename='api')
app_name = 'assets'
urlpatterns = [
    path('assets/', views.AssetsView.as_view(), name='asset-list'),
]