
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress
from students.models import Student, StudyTask

def advance_plan():
    print("=== ADVANCING PLAN SURGERY ===")
    student = Student.objects.get(id=10)
    
    # 1. Force Complete "Pozitif Tam Sayılar" (ID: 2430)
    topic_pozitif = Topic.objects.get(id=2430)
    prog, created = StudentProgress.objects.get_or_create(student=student, topic=topic_pozitif)
    prog.is_completed = True
    prog.save()
    print(f"Topic 2430 (Pozitif) status: {prog.is_completed}")
    
    # 2. Verify "Asal Çarpanlar" (ID: 2431) status
    topic_asal = Topic.objects.get(id=2431)
    prog_asal = StudentProgress.objects.filter(student=student, topic=topic_asal).first()
    print(f"Topic 2431 (Asal) status: {prog_asal.is_completed if prog_asal else 'NOT STARTED'}")

    # 3. Clear Active Tasks
    deleted_count = StudyTask.objects.filter(student=student, date__gte=date.today()).delete()
    print(f"Deleted {deleted_count[0]} future tasks.")
    
    # 4. Check Academic Scope
    from coaching.ai_service import AICoachingService
    ai = AICoachingService(student)
    m, w, topics = ai._get_academic_week_scope()
    print(f"Current Academic Scope: Month {m}, Week {w}")
    
    # 5. Simulate Next Topic Selection
    math_topics = [t for t in topics if t.subject.id == 1]
    completed_topic_ids = set(StudentProgress.objects.filter(student=student, is_completed=True).values_list('topic_id', flat=True))
    incomplete = [t for t in math_topics if t.id not in completed_topic_ids]
    
    print("\nMath Topics in this Week:")
    for t in math_topics:
        status = "COMPLETED" if t.id in completed_topic_ids else "PENDING"
        print(f"  ID: {t.id} | Order: {t.order} | {status} | {t.title}")
    
    if incomplete:
        print(f"\nNEXT TOPIC WILL BE: {incomplete[0].title} (ID: {incomplete[0].id})")
    else:
        print("\nALL TOPICS COMPLETED FOR THIS WEEK.")

if __name__ == "__main__":
    advance_plan()
