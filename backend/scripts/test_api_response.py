
from django.test import RequestFactory
from coaching.views import CurriculumViewSet
from students.models import Student, User
import json

# Setup
factory = RequestFactory()
view = CurriculumViewSet.as_view({'get': 'list_tree'})

# Get our target user
try:
    student = Student.objects.get(id=10)
    user = student.user
    print(f"Simulating request for: {student.full_name} (User: {user.username})")
except Exception as e:
    print(f"Error finding student: {e}")
    exit()

# Create Request
request = factory.get('/coaching/curriculum/?view=tree&subject=matematik')
request.user = user

# Execute View
response = view(request)
response.render()

# Parse Data
print(f"Status Code: {response.status_code}")
data = json.loads(response.content.decode('utf-8'))

# Inspect Month 9 (September) -> Week 1 -> Topic 1
found = False
for month in data.get('months', []):
    if month['id'] != 9: continue
    
    print(f"Checking Month: {month['name']}")
    for week in month.get('weeks', []):
        for topic in week.get('topics', []):
            if topic['id'] == 1:
                print(f"TARGET TOPIC FOUND: {topic['title']}")
                print(f" -> STATUS FROM API: {topic['status']}")
                print(f" -> FULL DATA: {topic}")
                found = True

if not found:
    print("Topic 1 not found in response structure!")

# Debug: Print first few lines of raw response if needed
# print(json.dumps(data, indent=2)[:500])
