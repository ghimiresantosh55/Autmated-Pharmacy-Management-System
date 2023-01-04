
from rest_framework import routers
from src.public import views
from django.urls import path, re_path, include
from .views import PublicUserRegisterView, PublicUserLoginView,  PublicUserChangePasswordView,PublicUserLogout,\
                 MedicineItemViewset,  GetAllCategoryViewset, PublicUserViewSet, PublicUserCustomerUpdateView,\
                    GetSuperCategoryViewset,  SkincareCategoryItemViewset,  BeautyCategoryItemViewset, HeathProductCategoryItemViewset,\
                         BloodTestItemViewset, BrandListViewset, BrandWiseItemViewset,  AddToCartListView,  ListPublicUserViewSet, \
                               SpecialOfferItemViewset, MostSaleItemViewSet


router = routers.DefaultRouter(trailing_slash=False)
router.register("skin-care-item", SkincareCategoryItemViewset)
router.register("beauty-item",  BeautyCategoryItemViewset)
router.register("health-product-item", HeathProductCategoryItemViewset)
router.register("blood-test-item",  BloodTestItemViewset)
router.register("medicine-item", MedicineItemViewset)
router.register("features-brand-item",  BrandWiseItemViewset)
router.register("brand-list", BrandListViewset)
router.register("all-category", GetAllCategoryViewset)
router.register("get-super-category",  GetSuperCategoryViewset)
router.register("user-app/register", PublicUserRegisterView)
router.register("user-app/public-users", PublicUserViewSet)
router.register("user-app/public-user-update",  PublicUserCustomerUpdateView)
router.register("add-to-cart",  AddToCartListView)
router.register("public-user-list",  ListPublicUserViewSet)
router.register('special-offer-item-list', SpecialOfferItemViewset)
router.register('top-sale-item-list',MostSaleItemViewSet, basename="top-item-sale")

urlpatterns = [
    path('user-app/login',  PublicUserLoginView.as_view(), name='UserLogin'),
    path('user-app/change-password/<int:pk>', PublicUserChangePasswordView.as_view(),
         name='auth_change_password'),
    
     path('user-app/logout', PublicUserLogout.as_view(), name="logout"),
  
    
       
] + router.urls