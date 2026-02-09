
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import StudentProgress, Topic
from students.models import Student

def check():
    print("--- PERSISTENCE CHECK ---")
    try:
        student = Student.objects.get(id=10)
    except:
        print("Student 10 MIA")
        return

    # Check T2430 specifically
    try:
        t = Topic.objects.get(id=2430)
        prog = StudentProgress.objects.filter(student=student, topic=t).first()
        print(f"Topic 2430: {t.title}")
        print(f"Progress Exists? {prog is not None}")
        if prog:
            print(f"Is Completed? {prog.is_completed}")
            print(f"Topic ID in Progress: {prog.topic.id}")
            print(f"Topic ID in DB: {prog.topic_id}")
    except Topic.DoesNotExist:
        print("Topic 2430 MIA")

    # Check Total Completed
    count = StudentProgress.objects.filter(student=student, is_completed=True).count()
    print(f"Total Completed Progress Records for Student 10: {count}")

if __name__ == "__main__":
    check()
