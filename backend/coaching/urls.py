from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CoachingViewSet, CurriculumViewSet

router = DefaultRouter()
router.register(r'coach', CoachingViewSet, basename='coach')
router.register(r'curriculum', CurriculumViewSet, basename='curriculum')

urlpatterns = [
    path('', include(router.urls)),
]
