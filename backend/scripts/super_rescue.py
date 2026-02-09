
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress, Subject

def super_rescue():
    sid = 10
    student = Student.objects.get(id=sid)
    config = student.coaching_config
    m = config.current_academic_month
    w = config.current_academic_week
    
    print(f"--- SUPER RESCUE FOR STUDENT {sid} (Month {m}, Week {w}) ---")
    
    # 3. Verify all math topics for M9 W1
    math_topics = Topic.objects.filter(subject__name="Matematik", month=m, week=w).order_by('order')
    print("\n[M9 W1 MATH TOPICS]")
    for mt in math_topics:
        print(f"ID: {mt.id} | Order: {mt.order} | Title: {mt.title}")

    # 1. Clean up duplicate progress
    # ...
    # If a student has progress on multiple topics with the same title for the same subject,
    # we should consolidate it to the CURRENT month/week or at least ensure titles match.
    
    all_progs = StudentProgress.objects.filter(student=student, is_completed=True).select_related('topic', 'topic__subject')
    
    for p in all_progs:
        # If the progress is NOT in the current week, check if it SHOULD be.
        # Actually, for the "first" topic of the year, we want it in Month 9 Week 1.
        
        # Let's find the 'canonical' topic for this title/subject in the ACTIVE month/week.
        target_topic = Topic.objects.filter(
            subject=p.topic.subject,
            month=m,
            week=w,
            title=p.topic.title
        ).first()
        
        if target_topic and target_topic.id != p.topic.id:
            print(f"Relocating progress: '{p.topic.title}' ({p.topic.subject.name})")
            print(f"  From: ID {p.topic.id} (M:{p.topic.month} W:{p.topic.week})")
            print(f"  To:   ID {target_topic.id} (M:{target_topic.month} W:{target_topic.week})")
            
            StudentProgress.objects.update_or_create(
                student=student,
                topic=target_topic,
                defaults={'is_completed': True, 'completed_at': p.completed_at}
            )
            # Delete the old one
            p.delete()

    # 2. Force mark tasks as done if they were completed but sync failed
    # Find tasks for today that are 'done' but not synced
    for t in StudyTask.objects.filter(student=student, status='done'):
        if t.topic_id:
            topic = Topic.objects.get(id=t.topic_id)
            StudentProgress.objects.update_or_create(
                student=student,
                topic=topic,
                defaults={'is_completed': True, 'completed_at': t.completed_at or timezone.now()}
            )
            print(f"Fixed sync for Task {t.id}: {t.topic_name}")

    print("--- RESCUE COMPLETE ---")

if __name__ == "__main__":
    super_rescue()
