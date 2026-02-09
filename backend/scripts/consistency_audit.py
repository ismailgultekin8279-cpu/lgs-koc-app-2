import requests
import time

URL = "http://localhost:8000/api/coaching/10/status/"
# Note: This requires the server to be running and no auth or using a known token.
# Since I'm in the CLI, I'll use the shell approach instead.

import os
import django
import sys

sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.views import CoachingViewSet
from rest_framework.test import APIRequestFactory

def consistency_check():
    factory = APIRequestFactory()
    view = CoachingViewSet.as_view({'get': 'status'})
    
    print("Running Consistency Check (5 iterations)...")
    for i in range(5):
        request = factory.get('/api/coaching/10/status/')
        response = view(request, pk=10)
        data = response.data
        print(f"Iteration {i+1}: Message='{data['message'][:60]}...' | Critical Count={len(data.get('weights', {}))}")
        time.sleep(0.5)

if __name__ == "__main__":
    consistency_check()
