
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import CoachingConfig, Topic, StudentProgress

def diagnose():
    student_id = 10 # Assuming this is the test student
    try:
        student = Student.objects.get(id=student_id)
        config = student.coaching_config
        print(f"--- Student: {student.full_name} ---")
        print(f"Month: {config.current_academic_month}, Week: {config.current_academic_week}")
        print(f"Week Started At: {config.week_started_at}")
        print(f"Today: {date.today()}")
        
        if config.week_started_at:
            days_passed = (date.today() - config.week_started_at).days
            print(f"Days Passed: {days_passed}")
            
        print("\n--- Current Study Tasks (Uncompleted) ---")
        tasks = StudyTask.objects.filter(student=student, status='pending').order_by('date', 'order')[:10]
        for t in tasks:
            print(f"Date: {t.date} | Order: {t.order} | {t.subject}: {t.topic_name}")
            
        print("\n--- Completed Progress ---")
        progs = StudentProgress.objects.filter(student=student, is_completed=True).select_related('topic')
        for p in progs:
            print(f"Completed: {p.topic.subject.name} - {p.topic.title}")

        print("\n--- Curriculum Check (Math Sept Week 1) ---")
        math_topics = Topic.objects.filter(subject__name="Matematik", month=9, week=1).order_by('order')
        for t in math_topics:
            print(f"Order {t.order}: {t.title}")

    except Exception as e:
        print(f"Error: {e}")

diagnose()
