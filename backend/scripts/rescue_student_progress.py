
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress

def rescue_student_10():
    sid = 10
    student = Student.objects.get(id=sid)
    config = student.coaching_config
    m = config.current_academic_month
    w = config.current_academic_week
    
    print(f"Rescuing Student {sid} (Active Month {m}, Week {w})...")
    
    # Get all progress records for this student
    progs = StudentProgress.objects.filter(student=student, is_completed=True)
    
    for p in progs:
        if p.topic.month != m or p.topic.week != w:
            # This is a mismatch. Let's see if there's a corresponding topic in the active week.
            matching_topic = Topic.objects.filter(
                subject=p.topic.subject,
                month=m,
                week=w,
                title=p.topic.title # This works because I standardized titles!
            ).first()
            
            if matching_topic:
                print(f"Moving progress: '{p.topic.title}' from M:{p.topic.month} to M:{m} (Active)")
                StudentProgress.objects.update_or_create(
                    student=student,
                    topic=matching_topic,
                    defaults={'is_completed': True, 'completed_at': p.completed_at}
                )
                # Optionally delete the old one or leave it? User likely wants it to count for "now".
                # Let's delete the old one to avoid confusion.
                p.delete()
    
    print("Rescue complete.")

rescue_student_10()
