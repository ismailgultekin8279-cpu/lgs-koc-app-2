import os
import django
import sys
import json
from datetime import date

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.services import CoachingService
from coaching.models import CoachingConfig

def verify_final():
    student = Student.objects.get(id=10)
    service = CoachingService(student)
    
    print("Triggering Fresh Plan Generation...")
    # Force fresh generation
    tasks = service.generate_daily_plan()
    
    # Reload config
    config = CoachingConfig.objects.get(student=student)
    print(f"Final Message in DB: {config.last_coach_message}")
    
    # Check tasks
    today = date.today()
    todays_tasks = StudyTask.objects.filter(student=student, date=today).order_by('order')
    print(f"Tasks for Today ({today}):")
    found_crit = False
    for t in todays_tasks:
        is_crit = "Kritik" in t.topic_name
        if is_crit: found_crit = True
        print(f" - [{t.subject}] {t.topic_name} (Type: {t.task_type}) {'[CRITICAL!]' if is_crit else ''}")
        
    if "Matematik" in config.last_coach_message and found_crit:
        print("\nSUCCESS: All systems green. Matematik prioritized and labeled.")
    else:
        print("\nPARTIAL SUCCESS: Check logic if criticality labels or message missed.")

if __name__ == "__main__":
    verify_final()
