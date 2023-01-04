"""ss_allowance URL Configuration

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )
from tenant.views import TenantMapView
from easy_care import settings
from rest_framework_simplejwt import views as jwt_views
# from .Jwt_views import CustomTokenObtainPairView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    # path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),

    #Optional UI:
    path('schema', SpectacularAPIView.as_view(), name='schema'),
    path('doc', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    #Tenant
    path('api/', include('src.api.urls')),
    path('history/', include('log_app.urls')),
    path('branches', TenantMapView.as_view()),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL,\
document_root=settings.STATIC_ROOT)
