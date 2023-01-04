from rest_framework import routers
from django.urls import path

from .views import smsView

router = routers.DefaultRouter(trailing_slash=False)


urlpatterns = [
    path('send', smsView.as_view())
]

