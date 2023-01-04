from rest_framework import routers

from .views import  SaveBloodTestOrderMainViewSet, DeleteBloodTestOrderOrderViewSet, QuickUpdateBloodOrderViewSet
from django.urls import path, include
    

router = routers.DefaultRouter(trailing_slash=False)

# Check where this URL is used???
router.register("save-blood-test-order", SaveBloodTestOrderMainViewSet)
router.register("blood-test-order",  QuickUpdateBloodOrderViewSet)


urlpatterns = [
    path('delete-blood-test-order/<int:pk>',  DeleteBloodTestOrderOrderViewSet.as_view()),
    
] + router.urls
