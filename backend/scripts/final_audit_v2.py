import os
import django
import sys
import json

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.services import CoachingService
from coaching.models import CoachingConfig

def final_audit():
    student = Student.objects.get(id=10)
    service = CoachingService(student)
    
    # Trigger plan generation
    print("Trigging plan generation...")
    tasks = service.generate_daily_plan()
    
    # Reload config to check message
    config = CoachingConfig.objects.get(student=student)
    print(f"\nFinal Coach Message: |{config.last_coach_message}|")
    
    # Check today's tasks for "Kritik" labels
    from datetime import date
    today_tasks = StudyTask.objects.filter(student=student, date=date.today())
    print(f"\nToday's Tasks ({date.today()}):")
    for t in today_tasks:
        print(f" - {t.subject}: {t.topic_name} (Type: {t.task_type})")

if __name__ == "__main__":
    final_audit()
