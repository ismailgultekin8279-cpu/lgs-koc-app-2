
from students.models import StudyTask
from coaching.models import StudentProgress
from rest_framework.test import APIRequestFactory, force_authenticate
from students.views import StudyTaskViewSet
import json

sid = 10
print(f"--- BI-DIRECTIONAL SYNC VERIFICATION FOR STUDENT {sid} ---")

# Find the Pozitif task
task = StudyTask.objects.filter(student_id=sid, topic_name__icontains="Pozitif").first()
if not task:
    print("Test task not found!")
    exit()

print(f"Testing with Task: '{task.topic_name}' (ID: {task.id})")

factory = APIRequestFactory()
view = StudyTaskViewSet.as_view({'post': 'toggle_status'})

def check_topic_status(topic_id):
    sp = StudentProgress.objects.filter(student_id=sid, topic_id=topic_id).first()
    return sp.is_completed if sp else False

# 1. Start State
print(f"Initial State: Task Status={task.status}, Topic Completed={check_topic_status(task.id)}")

# 2. Toggle to DONE
print("\nToggling to DONE...")
request = factory.post(f'/students/tasks/{task.id}/toggle_status/')
force_authenticate(request, user=task.student.user)
response = view(request, pk=task.id)
task.refresh_from_db()
print(f"New Task Status: {task.status}")
print(f"New Topic Completed: {check_topic_status(1)}") # Topic ID 1 is Pozitif

# 3. Toggle back to PENDING
print("\nToggling back to PENDING...")
request = factory.post(f'/students/tasks/{task.id}/toggle_status/')
force_authenticate(request, user=task.student.user)
response = view(request, pk=task.id)
task.refresh_from_db()
print(f"New Task Status: {task.status}")
print(f"New Topic Completed: {check_topic_status(1)}")

if task.status == 'pending' and not check_topic_status(1):
    print("\nSUCCESS: Bi-directional sync verified!")
else:
    print("\nFAILURE: Sync logic did not work as expected.")
