
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress
from students.models import Student, StudyTask
from students.views import StudyTaskViewSet

def diagnose():
    student_id = 10
    student = Student.objects.get(id=student_id)
    print(f"--- DIAGNOSTIC FOR STUDENT {student_id} ---")
    
    # 1. Find the current Math task
    task = StudyTask.objects.filter(student=student, subject='Matematik', status='pending').first()
    if not task:
        print("No pending math task found. Creating one for 'Pozitif'...")
        t_poz = Topic.objects.get(id=2430)
        task = StudyTask.objects.create(
            student=student, topic_id=t_poz.id, topic_name=t_poz.title,
            subject='Matematik', date=date.today(), status='pending'
        )
    
    print(f"Testing Task: {task.topic_name} (ID: {task.id}, TopicID: {task.topic_id})")
    
    # 2. Simulate the Toggle
    print("\nSimulating TOGGLE to 'done'...")
    view = StudyTaskViewSet()
    view._sync_to_curriculum(task, True)
    
    # 3. Check StudentProgress
    sp = StudentProgress.objects.filter(student=student, topic_id=task.topic_id).first()
    if sp:
        print(f"StudentProgress Entry Found. ID: {sp.id}, IsCompleted: {sp.is_completed}")
    else:
        print("CRITICAL: StudentProgress record NOT FOUND after sync!")
        
    # Check by title matching if ID failed
    if not sp or not sp.is_completed:
        print("\nChecking why matching might have failed...")
        import re
        clean_name = re.sub(r'\(.*?\)', '', task.topic_name).strip()
        print(f"  Cleaned Task Name: '{clean_name}'")
        
        # Look for potential topics
        topics = Topic.objects.filter(subject__name='Matematik')
        for t in topics[:5]:
            clean_t = re.sub(r'\(.*?\)', '', t.title).strip()
            print(f"  Topic ID {t.id}: '{t.title}' -> Cleaned: '{clean_t}'")
            if clean_t == clean_name:
                print(f"  MATCH FOUND ON ID {t.id}!")

if __name__ == "__main__":
    diagnose()
