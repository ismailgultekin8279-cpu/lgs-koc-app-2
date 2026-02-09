
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.models import Topic, StudentProgress
from coaching.ai_service import AICoachingService

sid = 10
student = Student.objects.get(id=sid)
service = AICoachingService(student)

def test_scope():
    print(f"--- ACADEMIC WEEK SCOPE TEST ---")
    m, w, topics = service._get_academic_week_scope()
    print(f"Target: Month {m}, Week {w}")
    print(f"Topics found: {list(topics.values_list('title', flat=True))}")
    
    # 1. Simulate finishing ONE topic in Week 1
    if topics.exists():
        t1 = topics.first()
        StudentProgress.objects.update_or_create(student=student, topic=t1, defaults={'is_completed': True})
        print(f"\n[Action] Marked '{t1.title}' as COMPLETED.")
        
        m2, w2, topics2 = service._get_academic_week_scope()
        print(f"New Target: Month {m2}, Week {w2}")
        if m == m2 and w == w2:
            print("SUCCESS: Still locked to Week 1 because other topics remain.")
        else:
            print("FAILURE: Jumped to next week prematurely.")

    # 2. Simulate finishing ALL topics in Week 1
    for t in topics:
        StudentProgress.objects.update_or_create(student=student, topic=t, defaults={'is_completed': True})
    
    print("\n[Action] Marked ALL Week 1 topics as COMPLETED.")
    m3, w3, topics3 = service._get_academic_week_scope()
    print(f"Next Target: Month {m3}, Week {w3}")
    if (m3 > m if m < 12 else m3 < m) or w3 > w:
         print("SUCCESS: Correctly moved to the next uncompleted week.")
    else:
         print("STAYED: If no topics in week 2, might stay or return None.")

# Clean up before test
StudentProgress.objects.filter(student=student).delete()
test_scope()
