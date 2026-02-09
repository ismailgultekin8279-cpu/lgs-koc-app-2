
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress, Subject

def final_check():
    sid = 10
    student = Student.objects.get(id=sid)
    config = student.coaching_config
    m = config.current_academic_month
    w = config.current_academic_week
    today = timezone.now().date()
    
    print(f"--- FINAL STATE CHECK (M:{m} W:{w}) ---")
    
    # Check Math Order 0
    math_subj = Subject.objects.filter(name="Matematik").first()
    topic_0 = Topic.objects.filter(subject=math_subj, month=m, week=w, order=0).first()
    
    if topic_0:
        prog = StudentProgress.objects.filter(student=student, topic=topic_0).first()
        print(f"Topic 0: {topic_0.title} (ID: {topic_0.id})")
        print(f"  Status: {'DONE' if prog and prog.is_completed else 'PENDING'}")
    
    # Check Today's Tasks
    tasks = StudyTask.objects.filter(student=student, date=today).order_by('order')
    print("\n--- TODAY'S TASKS ---")
    for t in tasks:
        print(f"ID: {t.id} | Status: {t.status} | TopicID: {t.topic_id} | Name: {t.topic_name}")

if __name__ == "__main__":
    final_check()
