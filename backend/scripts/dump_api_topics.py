
from rest_framework.test import APIRequestFactory, force_authenticate
from coaching.views import CurriculumViewSet
from students.models import Student
import json

print("--- FULL DUMP API REQUEST ---")
factory = APIRequestFactory()
view = CurriculumViewSet.as_view({'get': 'list_tree'})
student = Student.objects.get(id=10)
request = factory.get('/coaching/curriculum/', {'view': 'tree', 'subject': 'matematik'}, format='json')
force_authenticate(request, user=student.user)

response = view(request)
response.render()
data = json.loads(response.content.decode('utf-8'))

print(f"Subject: {data.get('subject')}")
for m in data.get('months', []):
    print(f"Month: {m.get('name')} (ID: {m.get('id')})")
    for w in m.get('weeks', []):
        for t in w.get('topics', []):
            print(f" - Topic: {t.get('title')} (ID: {t.get('id')}) REQ_STATUS: {t.get('status')}")
