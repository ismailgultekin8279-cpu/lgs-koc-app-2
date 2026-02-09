
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress, Subject

def reset_to_week1():
    sid = 10
    student = Student.objects.get(id=sid)
    config = student.coaching_config
    
    # 1. Ensure active month/week is 9/1
    config.current_academic_month = 9
    config.current_academic_week = 1
    config.save()
    print("Locked student 10 to Month 9, Week 1.")

    # 2. Find ALL 'Pozitif' topics in Month 9 Week 1
    math_subj = Subject.objects.filter(name="Matematik").first()
    topics = Topic.objects.filter(subject=math_subj, month=9, week=1, title="Pozitif Tam Say\u0131lar\u0131n \u00c7arpanlar\u0131")
    
    for t in topics:
        StudentProgress.objects.update_or_create(
            student=student,
            topic=t,
            defaults={'is_completed': True, 'completed_at': timezone.now()}
        )
        print(f"Marked ID {t.id} as GREEN.")

    # 3. Clear today's tasks to force a fresh plan generation
    StudyTask.objects.filter(student=student, date=timezone.now().date()).delete()
    print("Cleared today's tasks. Next 'Plan Refresh' will start from the next topic.")

if __name__ == "__main__":
    reset_to_week1()
