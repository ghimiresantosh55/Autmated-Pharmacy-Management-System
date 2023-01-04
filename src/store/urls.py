from rest_framework.urls import path
from .views import LocationListApiView, LocationUpdateApiView, LocationCheckApiView


urlpatterns = [
    path("location", LocationListApiView.as_view()),
    path("update-location", LocationUpdateApiView.as_view() ),
    path("check-location", LocationCheckApiView.as_view() )
]
