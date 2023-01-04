from rest_framework import routers
from django.urls import path, include

from .views import UnitViewSet, GenericNameViewSet, ItemViewSet
from .views import  SuperCategoryViewSet, ProductCategoryViewSet, MedicineCategoryViewSet,\
     MedicineFormViewSet, PoPriorityViewSet, StrengthViewSet , ItemUnitViewSet,  GenericStrengthViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register("unit", UnitViewSet)
router.register("item-unit", ItemUnitViewSet)
router.register("generic-name", GenericNameViewSet)
router.register("item", ItemViewSet)
router.register("super-category", SuperCategoryViewSet)
router.register("product-category", ProductCategoryViewSet)
router.register("medicine-category", MedicineCategoryViewSet)
router.register("medicine-form", MedicineFormViewSet)
router.register("po-priority", PoPriorityViewSet)
router.register("strength", StrengthViewSet)
router.register("generic-name-strength", GenericStrengthViewSet)

urlpatterns = [
    path('', include(router.urls))
    
]
