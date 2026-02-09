
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import StudyTask
from coaching.models import Topic

def check_today():
    sid = 10
    today = timezone.now().date()
    tasks = StudyTask.objects.filter(student_id=sid, date=today).order_by('order')
    print(f"--- TASKS FOR {today} (STUDENT {sid}) ---")
    if not tasks.exists():
        print("No tasks for today.")
    for t in tasks:
        topic_info = ""
        if t.topic_id:
            try:
                topic = Topic.objects.get(id=t.topic_id)
                topic_info = f" | [CURRICULUM M:{topic.month} W:{topic.week} Ord:{topic.order} ID:{topic.id}]"
            except Topic.DoesNotExist:
                topic_info = " | [TOPIC NOT FOUND]"
        print(f"ID: {t.id} | Status: {t.status} | TopicID: {t.topic_id} | Name: {t.topic_name}{topic_info}")

if __name__ == "__main__":
    check_today()
