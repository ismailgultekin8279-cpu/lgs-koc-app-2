import os
import django
from datetime import date
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.services import CoachingService
from django.conf import settings

print(f"DEBUG: GEMINI_API_KEY from settings: {getattr(settings, 'GEMINI_API_KEY', None)}")

student = Student.objects.first()
if student:
    print(f"Testing for student: {student.full_name}")
    # Force new plan by deleting today's tasks
    StudyTask.objects.filter(student=student, date=date.today()).delete()
    
    service = CoachingService(student)
    tasks = service.generate_daily_plan()
    
    print("--- GENERATED TASKS ---")
    for t in tasks:
        print(f"Topic: {t.topic_name} | Type: {t.task_type}")
else:
    print("No student found")
