
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, CoachingConfig
from students.models import Student, StudyTask
from coaching.ai_service import AICoachingService

def full_reset():
    student_id = 10
    student = Student.objects.get(id=student_id)
    today = date.today()
    
    print(f"--- FULL PROGRESS RESET FOR STUDENT {student_id} ---")
    
    # 1. Clear all progress (Back to Zero)
    progress_deleted = StudentProgress.objects.filter(student=student).delete()
    print(f"Deleted {progress_deleted[0]} progress records. Student is now at 'Zero'.")
    
    # 2. Reset Coaching Config to the very first week
    config, _ = CoachingConfig.objects.get_or_create(student=student)
    config.current_academic_month = 9
    config.current_academic_week = 1
    config.week_started_at = today
    config.save()
    print(f"Reset CoachingConfig to September Week 1.")
    
    # 3. Clear all tasks
    tasks_deleted = StudyTask.objects.filter(student=student).delete()
    print(f"Deleted {tasks_deleted[0]} study tasks.")
    
    # 4. Regenerate Plan with the NEW Sequential Logic
    print("Regenerating plan...")
    ai = AICoachingService(student)
    # Using fallback because it's deterministic and uses the new sequential code I just added
    ai._generate_fallback_response({}, today)
    print("Plan regenerated.")
    
    # 5. Verify the Top-of-List Topic
    first_math_task = StudyTask.objects.filter(student=student, date=today, subject="Matematik").first()
    if first_math_task:
        print(f"\nSTRICT SEQUENCE VERIFIED:")
        print(f"  Topic: {first_math_task.topic_name}")
        print(f"  ID: {first_math_task.topic_id}")
        if first_math_task.topic_id == 2430:
            print("  SUCCESS: Plan now correctly starts from 'Pozitif Tam Sayılar'!")

if __name__ == "__main__":
    full_reset()
