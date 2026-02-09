
import os
import sys
import django
import json
from django.test import RequestFactory
from rest_framework.test import force_authenticate

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress
from students.models import Student
from coaching.views import CurriculumViewSet
from django.contrib.auth.models import User

def audit_pozitif():
    print("--- 🔍 AUDIT: POZITIF TAM SAYILAR ---")
    
    try:
        student = Student.objects.get(id=10)
        print(f"👤 Student: {student.full_name} (ID: 10)")
    except Student.DoesNotExist:
        print("❌ Student 10 NOT FOUND")
        return

    # 1. Database Check
    print("\n[Database State]")
    pozitif_topics = Topic.objects.filter(title__icontains="Pozitif").order_by('id')
    
    if not pozitif_topics.exists():
        print("❌ No topics found with 'Pozitif' in title!")
    
    found_completed = False
    for t in pozitif_topics:
        prog = StudentProgress.objects.filter(student=student, topic=t).first()
        status_str = "Completed ✅" if (prog and prog.is_completed) else "Incomplete ❌"
        if prog and prog.is_completed:
            found_completed = True
        
        print(f"  • ID: {t.id} | Month: {t.month} | Week: {t.week} | Title: '{t.title}' -> {status_str}")
        if prog:
            print(f"    (Progress ID: {prog.id}, IsCompleted: {prog.is_completed})")

    # 2. Config Check
    conf = student.coaching_config
    print(f"\n[Academic Config] Month: {conf.current_academic_month}, Week: {conf.current_academic_week}")

    # 3. API Response Simulation
    print("\n[API Simulation: GET /coaching/curriculum/?view=tree&subject=matematik]")
    user = User.objects.get(username="iso")
    factory = RequestFactory()
    view = CurriculumViewSet.as_view({'get': 'list'})
    request = factory.get('/coaching/curriculum/', {'view': 'tree', 'subject': 'matematik'})
    force_authenticate(request, user=user)
    
    response = view(request)
    if response.status_code == 200:
        data = response.data
        # Dig into the structure to find the topic status
        # Trigger: we need to know what the FRONTEND sees.
        
        # Structure is usually: { months: [ { weeks: [ { topics: [ ... ] } ] } ] } 
        # OR list of subjects? Let's assume the dict structure based on previous reads.
        
        if isinstance(data, dict) and 'months' in data:
            found_in_api = False
            for m in data['months']:
                for w in m['weeks']:
                    for t in w['topics']:
                        if "pozitif" in t['title'].lower():
                            print(f"  API -> ID: {t['id']} | Title: '{t['title']}' | Status: {t['status']}")
                            found_in_api = True
                            
            if not found_in_api:
                print("❌ 'Pozitif' topic NOT FOUND in API response structure!")
        else:
            print(f"⚠️ Unexpected API Data Type: {type(data)}")
            # print(data) 
    else:
        print(f"❌ API Failed: {response.status_code}")

if __name__ == "__main__":
    audit_pozitif()
