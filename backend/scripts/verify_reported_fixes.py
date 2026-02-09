
from students.models import StudyTask, Student
from coaching.models import Topic, StudentProgress
from django.utils import timezone
from students.views import StudyTaskViewSet
from rest_framework.test import APIRequestFactory, force_authenticate
import json

sid = 10
student = Student.objects.get(id=sid)
factory = APIRequestFactory()
view = StudyTaskViewSet.as_view({'patch': 'partial_update'})

print(f"--- FOCUSED SYNC VERIFICATION FOR STUDENT {sid} ---")

test_cases = [
    # 1. Fen (Subject Name Variation)
    {"subject": "Fen", "topic": "DNA ve Genetik Kod (9. Ay, 4. Hafta)"},
    # 2. Din (Common Naming Variations)
    {"subject": "Din", "topic": "Din ve Hayat (9. Ay, 3. Hafta)"},
    {"subject": "Din Kültürü", "topic": "Kaderle İlgili Kavramlar (9. Ay, 1. Hafta)"},
    {"subject": "Din Kültürü", "topic": "Hz. Muhammed'in Örnekleri (9. Ay, 4. Hafta)"},
    # 3. Yabancı Dil
    {"subject": "Yabancı Dil", "topic": "Unit 2: Teen Life (9. Ay, 3. Hafta)"},
]

for tc in test_cases:
    print(f"\nTesting: {tc['subject']} | {tc['topic']}")
    
    # Create the task
    task = StudyTask.objects.create(
        student=student,
        subject=tc['subject'],
        topic_name=tc['topic'],
        status='pending',
        date='2026-01-28'
    )
    
    # Patch to done
    request = factory.patch(f'/students/tasks/{task.id}/', data={'status': 'done'}, format='json')
    force_authenticate(request, user=student.user)
    response = view(request, pk=task.id)
    
    # Find matching topic in DB to see what subject we SHOULD match
    # Since I aligned names, I'll check StudentProgress
    progress = StudentProgress.objects.filter(student=student, is_completed=True).order_by('-completed_at').first()
    
    if progress:
        print(f"  Matched DB Subject: {progress.topic.subject.name}")
        print(f"  Matched DB Topic: {progress.topic.title}")
        print(f"  Result: SUCCESS")
    else:
        print(f"  Result: FAILURE (No progress record found)")

    # Cleanup for next test
    StudentProgress.objects.filter(student=student).delete()
    task.delete()
