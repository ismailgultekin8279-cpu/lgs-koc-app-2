
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, Subject
from students.models import Student

def final_check():
    print("=== FINAL STATUS CHECK ===")
    try:
        student = Student.objects.get(id=10)
        print(f"Student: {student.full_name} (ID: 10)")
        
        # 1. Check September Week 1 Matematik
        math = Subject.objects.get(slug='matematik')
        topics = Topic.objects.filter(subject=math, month=9, week=1).order_by('order')
        
        print(f"\nMatematik September Week 1 Topics:")
        for t in topics:
            prog = StudentProgress.objects.filter(student=student, topic=t).first()
            status = "✅ Completed" if prog and prog.is_completed else "❌ Pending"
            print(f"  ID: {t.id} | Status: {status} | Title: {t.title}")
            
        # 2. Check Daily Plan for Today
        from students.models import StudyTask
        today = date.today()
        # today = date(2026, 2, 4) # Yesterday's check
        tasks = StudyTask.objects.filter(student=student, date=today)
        print(f"\nDaily Tasks for {today}:")
        if not tasks.exists():
            # Check latest
            latest_date = StudyTask.objects.filter(student=student).order_by('-date').values_list('date', flat=True).first()
            print(f"  No tasks for today. Latest tasks were on {latest_date}:")
            tasks = StudyTask.objects.filter(student=student, date=latest_date)
            
        for task in tasks:
            print(f"  Task ID: {task.id} | Topic ID: {task.topic_id} | Name: {task.topic_name} | Status: {task.status}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    final_check()
