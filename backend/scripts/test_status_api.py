import os
import django
import sys
import json

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from coaching.views import CoachingViewSet

def test_status_api():
    factory = APIRequestFactory()
    user = User.objects.get(username='iso')
    view = CoachingViewSet.as_view({'get': 'status'})
    
    request = factory.get(f'/api/v1/coaching/coach/{user.student_profile.id}/status/')
    force_authenticate(request, user=user)
    
    response = view(request, pk=user.student_profile.id)
    print("API Response:")
    print(json.dumps(response.data, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_status_api()
