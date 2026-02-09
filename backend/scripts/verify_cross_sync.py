
from students.models import StudyTask, Student
from coaching.models import Topic, StudentProgress
from rest_framework.test import APIRequestFactory, force_authenticate
from students.views import StudyTaskViewSet
import json

sid = 10
print(f"--- CROSS-SUBJECT SYNC VERIFICATION FOR STUDENT {sid} ---")

# Subjects to test
test_scenarios = [
    {"subject": "Matematik", "topic_hint": "Pozitif"},
    {"subject": "Yabancı Dil", "topic_hint": "Friendship"},
    {"subject": "T.C. İnkılap Tarihi", "topic_hint": "Avrupa"},
]

factory = APIRequestFactory()
view = StudyTaskViewSet.as_view({'patch': 'partial_update'})
student = Student.objects.get(id=sid)

for sc in test_scenarios:
    print(f"\nTesting {sc['subject']}...")
    # Find/Create a task for this subject if not exists (demo purposes)
    task = StudyTask.objects.filter(student=student, subject=sc['subject']).first()
    if not task:
        # Create a dummy task for testing
        task = StudyTask.objects.create(
            student=student,
            subject=sc['subject'],
            topic_name=f"{sc['subject']} - {sc['topic_hint']} Study",
            date="2026-01-28",
            status="pending"
        )
    
    # 1. Reset
    task.status = 'pending'
    task.save()
    
    # 2. PATCH to done
    request = factory.patch(f'/students/tasks/{task.id}/', data={'status': 'done'}, format='json')
    force_authenticate(request, user=student.user)
    response = view(request, pk=task.id)
    
    # 3. Check Progress
    # We need to find which topic it matched
    # For now check if ANY topic in that subject is completed for this student
    completed = StudentProgress.objects.filter(student=student, topic__subject__name=sc['subject'], is_completed=True).exists()
    
    print(f"Response: {response.status_code}")
    print(f"Any {sc['subject']} Topic Completed: {completed}")
    
    if completed:
        print(f"SUCCESS: {sc['subject']} sync verified!")
    else:
        print(f"FAILURE: {sc['subject']} sync failed.")
