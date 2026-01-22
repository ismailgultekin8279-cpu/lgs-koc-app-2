from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoachingViewSet

router = DefaultRouter()
router.register(r'coach', CoachingViewSet, basename='coach')

urlpatterns = [
    path('', include(router.urls)),
]
