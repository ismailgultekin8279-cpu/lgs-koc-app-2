
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.models import CoachingConfig, Topic, StudentProgress

try:
    student = Student.objects.first()
    if not student:
        print("No student found!")
        exit()

    print(f"Resetting configuration for: {student.full_name}")

    config, _ = CoachingConfig.objects.get_or_create(student=student)
    
    # 1. Force Reset to Week 1
    config.current_academic_month = 9
    config.current_academic_week = 1
    config.week_started_at = date.today()
    config.save()
    
    print(f"Set to Month 9, Week 1. Started: {config.week_started_at}")

    # 2. Clear Progress for Week 2 (EBOB/EKOK) so they don't look 'completed'
    week2_topics = Topic.objects.filter(month=9, week=2)
    deleted_count, _ = StudentProgress.objects.filter(student=student, topic__in=week2_topics).delete()
    
    print(f"Cleared {deleted_count} progress records for Week 2 topics to ensure clean slate.")

    print("DONE: Student is now locked back into Week 1.")

except Exception as e:
    print(f"Error: {e}")
