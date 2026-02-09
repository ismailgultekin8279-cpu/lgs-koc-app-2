
from students.models import StudyTask
from coaching.models import StudentProgress
from rest_framework.test import APIRequestFactory, force_authenticate
from students.views import StudyTaskViewSet
import json

sid = 10
print(f"--- PATCH SYNC VERIFICATION FOR STUDENT {sid} ---")

# Find the Pozitif task
task = StudyTask.objects.filter(student_id=sid, topic_name__icontains="Pozitif").first()
if not task:
    print("Test task not found!")
    exit()

# Ensure it starts as pending
task.status = 'pending'
task.save()
StudentProgress.objects.filter(student_id=sid, topic_id=1).update(is_completed=False)

factory = APIRequestFactory()
view = StudyTaskViewSet.as_view({'patch': 'partial_update'})

def check_topic_status(topic_id):
    sp = StudentProgress.objects.filter(student_id=sid, topic_id=topic_id).first()
    return sp.is_completed if sp else False

print(f"Initial State: Task={task.status}, Topic Completed={check_topic_status(1)}")

# 1. Send PATCH status='done'
print("\nSending PATCH status='done'...")
request = factory.patch(f'/students/tasks/{task.id}/', data={'status': 'done'}, format='json')
force_authenticate(request, user=task.student.user)
response = view(request, pk=task.id)
print(f"Response Status: {response.status_code}")

task.refresh_from_db()
print(f"Post-PATCH Task Status: {task.status}")
print(f"Post-PATCH Topic Completed: {check_topic_status(1)}")

if task.status == 'done' and check_topic_status(1):
    print("\nSUCCESS: PATCH sync verified!")
else:
    print("\nFAILURE: Sync did not trigger on PATCH.")
