
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.models import CoachingConfig, Topic, StudentProgress

try:
    student = Student.objects.get(id=10)
    print(f"Force Resetting Student ID 10: {student.full_name}")

    config, _ = CoachingConfig.objects.get_or_create(student=student)
    
    # 1. Force Reset to Week 1
    config.current_academic_month = 9
    config.current_academic_week = 1
    config.week_started_at = date.today()
    config.save()
    
    print(f"Set to Month 9, Week 1. Started: {config.week_started_at}")

    # 2. Clear Progress for Week 2 topics
    # And actually, let's verify Week 1 topics are NOT complete or ensure we can see them.
    # The updated fallback looks at scope, which returns topics regardless of progress.
    # But just in case, let's un-complete Week 1 topics so they feel fresh.
    week1_topics = Topic.objects.filter(month=9, week=1)
    StudentProgress.objects.filter(student=student, topic__in=week1_topics).update(is_completed=False)
    print("Marked Week 1 topics as uncompleted (fresh start).")
    
    # Clear Week 2+ progress
    future_topics = Topic.objects.filter(month=9, week__gt=1)
    StudentProgress.objects.filter(student=student, topic__in=future_topics).delete()
    print("Deleted any future progress for Week 2+.")

    print("DONE: Student 10 locked to Week 1.")

except Exception as e:
    print(f"Error: {e}")
