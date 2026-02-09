
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress
from students.models import Student, StudyTask

def audit():
    student_id = 10
    print(f"--- AUDIT FOR STUDENT {student_id} ---")
    
    # 1. Curiculum for Sept Week 1
    math_topics = Topic.objects.filter(subject_id=1, month=9, week=1).order_by('order')
    completed_ids = set(StudentProgress.objects.filter(student_id=student_id, is_completed=True).values_list('topic_id', flat=True))
    
    print("\nCurriculum Topics (Sept Week 1):")
    for t in math_topics:
        status = "DONE" if t.id in completed_ids else "PENDING"
        print(f"  Order {t.order} | ID {t.id} | {status} | {t.title}")
        
    # 2. Today's Tasks
    today = date.today()
    tasks = StudyTask.objects.filter(student_id=student_id, date=today)
    print(f"\nTasks for today ({today}):")
    for t in tasks:
        print(f"  Task {t.id} | TopicID {t.topic_id} | Status {t.status} | {t.topic_name}")

if __name__ == "__main__":
    audit()
