from rest_framework import routers

from django.urls import path, include

from .views import CompanyViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("company", CompanyViewSet)


urlpatterns = [
    path('', include(router.urls))
]