
from rest_framework.test import APIRequestFactory, force_authenticate
from coaching.views import CurriculumViewSet
from students.models import Student
import json

print("--- CONCISE API CHECK ---")
factory = APIRequestFactory()
view = CurriculumViewSet.as_view({'get': 'list_tree'})
student = Student.objects.get(id=10)
request = factory.get('/coaching/curriculum/', {'view': 'tree', 'subject': 'matematik'}, format='json')
force_authenticate(request, user=student.user)

response = view(request)
response.render()
data = json.loads(response.content.decode('utf-8'))

print(f"Debug Student ID: {data.get('debug_student_id')}")
print(f"Total Months: {len(data.get('months', []))}")

found = False
for m in data.get('months', []):
    for w in m.get('weeks', []):
        for t in w.get('topics', []):
            if t.get('id') == 1:
                print(f"!!! TARGET TOPIC 1 FOUND !!!")
                print(f"Title: {t.get('title')}")
                print(f"Status: {t.get('status')}")
                found = True

if not found:
    print("Topic 1 NOT found in response.")
