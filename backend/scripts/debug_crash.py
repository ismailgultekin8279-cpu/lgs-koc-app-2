
import os
import sys
import django
from django.test import RequestFactory
from rest_framework.test import force_authenticate

# Setup
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.views import StudentViewSet, StudyTaskViewSet
from students.models import Student
from django.contrib.auth.models import User

def debug_crash():
    print("--- DEBUGGING DASHBOARD CRASH ---")
    
    # Get User/Student
    try:
        user = User.objects.get(username="iso") # Adjust if needed
        student = Student.objects.get(id=10)
        print(f"User: {user}, Student: {student}")
    except Exception as e:
        print(f"FAILED to get user/student: {e}")
        return

    factory = RequestFactory()

    # 1. Test Student Stats (Dashboard load)
    print("\n1. Testing Student Stats API...")
    try:
        view = StudentViewSet.as_view({'get': 'stats'})
        request = factory.get('/students/stats/')
        force_authenticate(request, user=user)
        response = view(request)
        print(f"Stats Response Code: {response.status_code}")
        if response.status_code != 200:
            print(f"Error Data: {response.data}")
    except Exception as e:
        print(f"CRASH in Stats: {e}")
        import traceback
        traceback.print_exc()

    # 2. Test Today's Tasks
    print("\n2. Testing Today's Tasks API...")
    try:
        view = StudyTaskViewSet.as_view({'get': 'today'})
        request = factory.get('/students/tasks/today/')
        force_authenticate(request, user=user)
        response = view(request)
        print(f"Tasks Response Code: {response.status_code}")
        if response.status_code != 200:
             print(f"Error Data: {response.data}")
    except Exception as e:
        print(f"CRASH in Tasks: {e}")
        import traceback
        traceback.print_exc()

    # 3. Test Generate Plan (User clicked this?)
    print("\n3. Testing Generate Plan API...")
    try:
        from coaching.views import CoachingViewSet
        view = CoachingViewSet.as_view({'post': 'generate_plan'})
        request = factory.post('/coaching/generate_plan/')
        force_authenticate(request, user=user)
        response = view(request)
        print(f"Generate Plan Response Code: {response.status_code}")
        if response.status_code != 200:
             print(f"Error Data: {response.data}")
    except Exception as e:
        print(f"CRASH in Generate Plan: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_crash()
