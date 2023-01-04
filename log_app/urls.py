from django.urls import path, include
from django.urls.resolvers import URLPattern
from django.views.generic.base import View

from log_app.views.user_group import CustomGroupHistoryViewset,CustomPermissionHistoryViewset, PermissionCategoryHistoryViewset
from .views.user import UserHistoryViewset
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)

# user_group_app 
router.register("custom-group-history", CustomGroupHistoryViewset)
router.register("custom-permission-history", CustomPermissionHistoryViewset)
router.register("permission-category-history", PermissionCategoryHistoryViewset)

# user_app
router.register("user-history",UserHistoryViewset)

urlpatterns = [
    path('', include(router.urls))
    # path('customer-history',CustomerHistoryListView_as.View(), basename="hello" )
]