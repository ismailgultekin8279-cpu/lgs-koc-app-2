
import os
import sys
import django
import json
from django.test import RequestFactory

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.views import CustomTokenObtainPairView
from django.contrib.auth.models import User

def debug_login():
    print("--- DEBUGGING LOGIN ---")
    
    # Ensure user exists and password is known (or reset it for test?)
    # We can't know the password. But we can check the VIEW logic directly.
    # Actually, CustomTokenObtainPairView inherits from TokenObtainPairView.
    # It likely overrides `post`.
    
    # Instead of full auth flow (needs password), let's inspect the Serializer logic used in the view.
    from students.serializers import CustomTokenObtainPairSerializer
    
    user = User.objects.get(username="iso")
    print(f"User: {user.username}")
    
    # Manually run the serializer's validation logic which usually returns the token + student data
    serializer = CustomTokenObtainPairSerializer()
    
    # We can't call `validate` without credentials. 
    # But we can check `get_token` mechanism if custom claims are added.
    
    refresh = serializer.get_token(user)
    print("Token Generated.")
    
    # Check if the view adds extra data in the response
    # CustomTokenObtainPairView usually overrides `post` or uses a custom serializer that overrides `validate`.
    
    print("\nSimulating Serializer Response Construction...")
    data = {}
    data['refresh'] = str(refresh)
    data['access'] = str(refresh.access_token)
    
    # Logic from CustomTokenObtainPairSerializer.validate usually does this:
    # student = ...
    # data['student'] = ...
    
    # Let's see the source code of the serializer first?
    # Or just try to instantiate the student serializer used there.
    from students.models import Student
    from students.serializers import StudentSerializer
    
    try:
        student = Student.objects.get(user=user)
        print(f"Linked Student: {student.full_name}")
        s_data = StudentSerializer(student).data
        print(f"Serialized Student Data Keys: {s_data.keys()}")
        print(f"Student ID in data: {s_data.get('id')}")
    except Student.DoesNotExist:
        print("❌ Student not linked!")

if __name__ == "__main__":
    debug_login()
