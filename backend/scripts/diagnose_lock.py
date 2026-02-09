
import os
import sys
import django
from datetime import date

# Set up path and settings
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import CoachingConfig, StudentProgress, Topic, Subject
from students.models import Student

def diagnose():
    sid = 10
    try:
        student = Student.objects.get(id=sid)
    except Student.DoesNotExist:
        print(f"Error: Student {sid} not found.")
        return

    config, _ = CoachingConfig.objects.get_or_create(student=student)
    today = date.today()
    
    m = config.current_academic_month
    w = config.current_academic_week
    started = config.week_started_at
    
    print(f"--- DIAGNOSIS FOR {student.full_name} ---")
    print(f"Active Scope: M:{m}, W:{w}")
    print(f"Week Started: {started}")
    
    if started:
        days_passed = (today - started).days
        print(f"Days Passed: {days_passed}")
    else:
        print("Week Started: None")

    # Check topics in this week
    topics = Topic.objects.filter(month=m, week=w)
    total = topics.count()
    completed = StudentProgress.objects.filter(student=student, topic__in=topics, is_completed=True).count()
    
    print(f"Week Topics: Total {total}, Completed {completed}")
    
    # Check Math Subject Specifically
    math_subj = Subject.objects.filter(name="Matematik").first()
    if math_subj:
        done_orders = sorted(list(StudentProgress.objects.filter(
            student=student, 
            topic__subject=math_subj, 
            topic__month=m, 
            topic__week=w, 
            is_completed=True
        ).values_list('topic__order', flat=True)))
        print(f"Math Completed Orders: {done_orders}")
    else:
        print("Math Subject not found!")

if __name__ == "__main__":
    diagnose()
