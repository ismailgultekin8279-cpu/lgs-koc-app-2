
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import StudyTask
from coaching.models import Topic, StudentProgress

def check_sync_gaps():
    sid = 10
    print(f"--- DETAILED AUDIT FOR STUDENT {sid} ---")
    
    tasks = StudyTask.objects.filter(student_id=sid).order_by('-date', 'order')[:30]
    print("\n[STUDY TASKS (LATEST 30)]")
    for t in tasks:
        print(f"ID: {t.id} | Date: {t.date} | Status: {t.status} | {t.subject}: {t.topic_name}")
        
    progs = StudentProgress.objects.filter(student_id=sid).select_related('topic', 'topic__subject')
    print("\n[ALL STUDENT PROGRESS RECORDS]")
    for p in progs:
        status = "🟢 COMPLETED" if p.is_completed else "⚪ PENDING"
        print(f"{status} | {p.topic.subject.name} | {p.topic.title} (ID: {p.topic.id})")

check_sync_gaps()
