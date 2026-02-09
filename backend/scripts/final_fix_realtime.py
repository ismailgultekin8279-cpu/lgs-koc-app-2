
import os
import django
import sys
from django.utils import timezone

# Setup Django
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.models import CoachingConfig, Topic, StudentProgress, Subject

def fix_student_10():
    try:
        student = Student.objects.get(id=10)
        print(f"✅ Student Found: {student.full_name}")
    except Student.DoesNotExist:
        print("❌ Student ID 10 Not Found!")
        return

    # 1. Get Config
    config, _ = CoachingConfig.objects.get_or_create(student=student)
    print(f"📅 Active Scope: Month {config.current_academic_month}, Week {config.current_academic_week}")

    # 2. Get the Math Subject
    try:
        math_subject = Subject.objects.get(name="Matematik")
    except Subject.DoesNotExist:
         # Fallback search
         math_subject = Subject.objects.filter(name__icontains="Matematik").first()
    
    if not math_subject:
        print("❌ 'Matematik' Subject NOT FOUND!")
        return

    print(f"📘 Subject: {math_subject.name} (ID: {math_subject.id})")

    # 3. Find the Target Topic for the Active Week
    # We look for Order 0 (The first topic)
    target_topics = Topic.objects.filter(
        subject=math_subject,
        month=config.current_academic_month,
        week=config.current_academic_week,
        order=0
    )

    if not target_topics.exists():
        print(f"❌ No Math topic found for M{config.current_academic_month} W{config.current_academic_week} Order 0")
        # Try to find ANY math topic for this week to default to
        target_topics = Topic.objects.filter(
            subject=math_subject,
            month=config.current_academic_month,
            week=config.current_academic_week
        ).order_by('order')
        
    if not target_topics.exists():
         print("❌ No Math topics AT ALL for this week.")
         return

    # 4. FIX: Mark ALL matching topics as completed (in case of duplicates)
    print(f"🔍 Found {target_topics.count()} target topic(s). Fixing now...")
    
    for t in target_topics:
        # Update or Create Progress
        prog, created = StudentProgress.objects.update_or_create(
            student=student,
            topic=t,
            defaults={
                'is_completed': True,
                'completed_at': timezone.now()
            }
        )
        action = "Created" if created else "Updated"
        print(f"  👉 {action} Progress for Topic ID {t.id}: '{t.title}' -> COMPLETED")

    print("\n✅ FIX COMPLETE. Please refresh the dashboard.")

if __name__ == "__main__":
    fix_student_10()
