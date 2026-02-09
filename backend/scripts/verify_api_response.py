
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.views import CurriculumViewSet
from django.test import RequestFactory
from rest_framework.test import force_authenticate
from django.contrib.auth.models import User
import json

def verify_api():
    print("=== DIRECT API VERIFICATION ===\n")
    
    # Get user
    user = User.objects.get(username="iso")
    
    # Create mock request
    factory = RequestFactory()
    request = factory.get('/coaching/curriculum/', {'view': 'tree', 'subject': 'matematik'})
    force_authenticate(request, user=user)
    
    # Call view
    view = CurriculumViewSet.as_view({'get': 'list'})
    response = view(request)
    
    print(f"API Status Code: {response.status_code}\n")
    
    if response.status_code == 200:
        data = response.data
        
        # Find Pozitif topics
        pozitif_found = False
        
        if isinstance(data, dict) and 'months' in data:
            for month in data['months']:
                month_name = month.get('name', month.get('id'))
                for week in month.get('weeks', []):
                    week_num = week.get('week_number')
                    for topic in week.get('topics', []):
                        if 'pozitif' in topic.get('title', '').lower():
                            pozitif_found = True
                            status_icon = "✅" if topic.get('status') == 'completed' else "❌"
                            print(f"{status_icon} Month: {month_name} | Week: {week_num}")
                            print(f"   ID: {topic.get('id')} | Title: {topic.get('title')}")  
                            print(f"   Status: {topic.get('status')}\n")
        
        if not pozitif_found:
            print("❌ NO POZITIF TOPICS FOUND IN API RESPONSE!")
    else:
        print(f"❌ API Error: {response.status_code}")

if __name__ == "__main__":
    verify_api()
