from rest_framework import permissions
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from django.contrib import admin
from rest_framework import routers
from django.urls import path, re_path, include
# from django.conf.urls import url
from assets import views
router = routers.DefaultRouter()
# router.register('assets', views.AssetsView.as_view(), basename='assets')
# router.register(r'api/assets/1', views.asset_detail, basename='api')
# from rest_framework.schemas import get_schema_view
schema_view = get_schema_view(
    openapi.Info(
        title="AssetMappr APIs",
        default_version='v1',
        description="Version 1 API for AssetMappr. ",
        terms_of_service="https://www.ourapp.com/policies/terms/",
        contact=openapi.Contact(email="assetmappr@andrew.cmu.edu"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
app_name = 'api'
urlpatterns = [

    # path('users/', views.AssetsView.as_view(), name='user-list'),
    path('api/', include(('assets.urls'))),
    path('', schema_view.with_ui('swagger', cache_timeout=0),
         name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc',
         cache_timeout=0), name='schema-redoc'),
    # path('', include(router.urls)),
    # path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # re_path(r'api/students', views.asset_list),
    # re_path(r'api/students/', views.asset_detail),
]
