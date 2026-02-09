
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress
from students.models import Student, StudyTask
from coaching.ai_service import AICoachingService

def fix_and_regen():
    student_id = 10
    student = Student.objects.get(id=student_id)
    today = date.today()
    
    print(f"--- FIX & REGEN FOR STUDENT {student_id} ---")
    
    # 1. Ensure Asal (2431) is DONE
    t_asal = Topic.objects.get(id=2431)
    sp, created = StudentProgress.objects.get_or_create(student=student, topic=t_asal)
    sp.is_completed = True
    sp.save()
    print(f"Topic 2431 (Asal) ensured as DONE.")
    
    # 2. Delete all tasks for today
    deleted = StudyTask.objects.filter(student=student, date=today).delete()
    print(f"Deleted {deleted[0]} tasks for today.")
    
    # 3. Regenerate
    print("Regenerating plan...")
    ai = AICoachingService(student)
    # Using fallback for speed and predictability in verification
    ai._generate_fallback_response({}, today)
    print("Plan regenerated.")
    
    # 4. Verify
    new_tasks = StudyTask.objects.filter(student=student, date=today, subject="Matematik")
    print("\nNew Math Tasks for Today:")
    for t in new_tasks:
        print(f"  ID:{t.id} | TopicID:{t.topic_id} | {t.topic_name}")
        if t.topic_id == 2432:
            print("SUCCESS: Advanced to Order 2 (Temel İşlem Yeteneği)!")
        else:
            print(f"STILL STUCK? TopicID is {t.topic_id}")

if __name__ == "__main__":
    fix_and_regen()
