
from rest_framework.test import APIRequestFactory, force_authenticate
from coaching.views import CurriculumViewSet
from students.models import Student
import json

print("--- SIMULATING AUTHENTICATED API REQUEST ---")

# Setup
factory = APIRequestFactory()
view = CurriculumViewSet.as_view({'get': 'list_tree'})

# Get user
try:
    student = Student.objects.get(id=10)
    user = student.user
    print(f"User: {user.username} (Student ID: {student.id})")
except:
    print("User/Student not found")
    exit()

# Create Request
request = factory.get('/coaching/curriculum/', {'view': 'tree', 'subject': 'matematik'}, format='json')
force_authenticate(request, user=user)

# Execute View
response = view(request)
response.render()

print(f"Response Status: {response.status_code}")

if response.status_code == 200:
    data = json.loads(response.content.decode('utf-8'))
    # Inspect
    found = False
    for month in data.get('months', []):
        if month['id'] != 9: continue
        for week in month.get('weeks', []):
            for topic in week.get('topics', []):
                if topic['id'] == 1:
                    print(f"TARGET TOPIC (ID:1) '{topic['title']}' STATUS: >>> {topic['status']} <<<")
                    found = True
    if not found:
        print("Topic 1 not found in JSON.")
else:
    print("Request failed.")
