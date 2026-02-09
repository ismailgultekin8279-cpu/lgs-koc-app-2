
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, CoachingConfig
from students.models import Student, StudyTask

def dump_state():
    student_id = 10
    student = Student.objects.get(id=student_id)
    print(f"=== FULL STATE DUMP FOR STUDENT {student_id} ===")
    
    # 1. Config
    config = getattr(student, 'coaching_config', None)
    if config:
        print(f"CONFIG: Month {config.current_academic_month}, Week {config.current_academic_week}, Started {config.week_started_at}")
    
    # 2. Completed Topics
    completed = StudentProgress.objects.filter(student=student, is_completed=True).order_by('topic__month', 'topic__week', 'topic__order')
    print(f"\nCOMPLETED TOPICS ({completed.count()}):")
    for cp in completed:
        t = cp.topic
        print(f"  ID:{t.id} | {t.subject.name} | Month:{t.month} | Week:{t.week} | Order:{t.order} | {t.title}")
        
    # 3. Tasks for Today
    today = date.today()
    tasks = StudyTask.objects.filter(student=student, date=today).order_by('id')
    print(f"\nTASKS FOR TODAY ({today}):")
    for t in tasks:
        print(f"  TaskID:{t.id} | TopicID:{t.topic_id} | Subject:{t.subject} | Status:{t.status} | Title:{t.topic_name}")
        
    # 4. Recent Task History (Last 20)
    print("\nRECENT TASK HISTORY (Last 20):")
    history = StudyTask.objects.filter(student=student).order_by('-id')[:20]
    for t in history:
        print(f"  ID:{t.id} | Date:{t.date} | TopicID:{t.topic_id} | Status:{t.status} | Title:{t.topic_name}")

if __name__ == "__main__":
    dump_state()
