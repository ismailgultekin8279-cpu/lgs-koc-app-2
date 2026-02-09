
import os
import django
import sys
from django.utils import timezone

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import StudentProgress, Topic
from students.models import Student

def fix_2430():
    print("=== SURGICAL FIX: Topic 2430 ===\n")
    
    try:
        student = Student.objects.get(id=10)
        topic = Topic.objects.get(id=2430)
    except Exception as e:
        print(f"❌ Error: {e}")
        return
    
    print(f"Student: {student.full_name}")
    print(f"Topic: {topic.title} (ID: 2430)\n")
    
    # Delete and recreate to ensure clean state
    deleted_count, _ = StudentProgress.objects.filter(
        student=student,
        topic=topic
    ).delete()
    
    print(f"Deleted {deleted_count} existing progress records\n")
    
    # Create new completed record
    prog = StudentProgress.objects.create(
        student=student,
        topic=topic,
        is_completed=True,
        completed_at=timezone.now()
    )
    
    print(f"✅ Created NEW Progress Record:")
    print(f"   ID: {prog.id}")
    print(f"   Is Completed: {prog.is_completed}")
    print(f"   Completed At: {prog.completed_at}\n")
    
    # Verify
    check = StudentProgress.objects.get(id=prog.id)
    print(f"Verification: {check.is_completed}")
    
    # Count total completed for this week
    from coaching.models import CoachingConfig
    config = student.coaching_config
    
    week_topics = Topic.objects.filter(
        month=config.current_academic_month,
        week=config.current_academic_week
    )
    
    completed_count = StudentProgress.objects.filter(
        student=student,
        topic__in=week_topics,
        is_completed=True
    ).count()
    
    print(f"\n📊 Week Completion: {completed_count}/{week_topics.count()} topics")

if __name__ == "__main__":
    fix_2430()
