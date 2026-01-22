from rest_framework.routers import DefaultRouter
from .views import StudentViewSet, ExamResultViewSet

router = DefaultRouter()
router.register(r"students", StudentViewSet, basename="students")
router.register(r"exam-results", ExamResultViewSet, basename="exam-results")

urlpatterns = router.urls
