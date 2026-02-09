
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress

def dump_state():
    sid = 10
    from students.models import Student, StudyTask
    from coaching.models import Topic, StudentProgress
    
    student = Student.objects.get(id=sid)
    config = student.coaching_config
    print(f"Student: {student.full_name}")
    print(f"Active Month: {config.current_academic_month}, Active Week: {config.current_academic_week}")
    
    tasks = StudyTask.objects.filter(student=student).order_by('-id')[:5]
    print("\n--- LATEST 5 TASKS (BY ID DESC) ---")
    for t in tasks:
        topic_info = ""
        if t.topic_id:
            try:
                topic = Topic.objects.get(id=t.topic_id)
                topic_info = f" | M:{topic.month} W:{topic.week} Ord:{topic.order}"
            except Topic.DoesNotExist:
                topic_info = " | [TOPIC NOT FOUND]"
        print(f"ID: {t.id} | Date: {t.date} | Status: {t.status} | Topic_ID: {t.topic_id}{topic_info} | Name: {t.topic_name}")
        
    progs = StudentProgress.objects.filter(student=student, is_completed=True).select_related('topic')
    print("\n--- COMPLETED IN CURRICULUM ---")
    for p in progs:
        print(f"ID: {p.topic.id} | M:{p.topic.month} W:{p.topic.week} Ord:{p.topic.order} | Title: {p.topic.title}")

dump_state()
