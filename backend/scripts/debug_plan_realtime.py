
import os
import sys
import django
import traceback

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.services import CoachingService
from coaching.views import CoachingViewSet
from students.models import Student
from rest_framework.test import APIRequestFactory

def debug_plan_realtime():
    print("--- DEBUGGING PLAN GENERATION REALTIME ---")
    try:
        student = Student.objects.get(id=10)
        print(f"Student: {student.full_name}")
    except Student.DoesNotExist:
        print("Student 10 not found")
        return

    # 1. Test Service Directly
    print("\n1. Testing CoachingService.generate_daily_plan()...")
    try:
        service = CoachingService(student)
        tasks = service.generate_daily_plan()
        print(f"✅ Service Success! Generated {len(tasks)} tasks.")
        for t in tasks:
            print(f" - {t.topic_name} (ID: {t.topic_id})")
    except Exception:
        print("❌ CRASH in Service:")
        traceback.print_exc()

    # 2. Test View Logic (Simulate Request)
    print("\n2. Testing CoachingViewSet.generate_plan() Logic...")
    try:
        factory = APIRequestFactory()
        request = factory.post(f'/coaching/coach/{student.id}/generate_plan/')
        view = CoachingViewSet.as_view({'post': 'generate_plan'})
        
        # We need to force standard view behavior
        response = view(request, pk=student.id)
        print(f"✅ View Success! Status: {response.status_code}")
        if response.status_code != 201:
            print("Response Data:", response.data)
    except Exception:
        print("❌ CRASH in View:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_plan_realtime()
