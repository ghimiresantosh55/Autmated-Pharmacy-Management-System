from rest_framework import routers

from django.urls import path, include

from .views import BloodTestCategoryViewSet, BloodTestViewSet, TestPackageViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("blood-test-category",BloodTestCategoryViewSet)
router.register("blood-test",BloodTestViewSet)
router.register("test-package",TestPackageViewSet)



urlpatterns = [
    path('', include(router.urls))
]