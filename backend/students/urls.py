from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register(r'tasks', views.StudyTaskViewSet)
router.register(r'exam-results', views.ExamResultViewSet)
router.register(r'', views.StudentViewSet)

urlpatterns = [
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', views.CustomTokenObtainPairView.as_view(), name='login'),
    path("", include(router.urls)), 
    path("start-session/", views.start_session),
    path("end-session/<int:student_id>/", views.end_session),
    path("coach-message/", views.coach_message),
    path("student-report/<int:student_id>/", views.student_report),
    path("daily-report", views.daily_report, name="daily-report"),
    path("weekly-report", views.weekly_report, name="weekly-report"),
    path("open-sessions", views.open_sessions, name="open-sessions"),
]
