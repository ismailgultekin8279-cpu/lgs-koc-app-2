
import os
import django
import sys
from django.utils import timezone

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import StudentProgress, Topic
from students.models import Student

def fix_all_duplicates():
    print("--- FIX ALL POPZITIF DUPLICATES ---")
    try:
        student = Student.objects.get(id=10)
    except:
        print("Student 10 MIA")
        return

    # 1. Find ALL variations of Pozitif
    # Use exact "Pozitif Tam Sayıların Çarpanları" just to be safe, or contains "Pozitif"
    topics = Topic.objects.filter(title__icontains="Pozitif")
    print(f"Found {topics.count()} topics containing 'Pozitif'")

    # 2. Mark ALL as completed
    updated_count = 0
    created_count = 0
    
    for t in topics:
        prog, created = StudentProgress.objects.update_or_create(
            student=student,
            topic=t,
            defaults={
                'is_completed': True,
                'completed_at': timezone.now()
            }
        )
        if created:
            created_count += 1
        else:
            updated_count += 1
            
    print(f"✅ DONE. Created: {created_count}, Updated: {updated_count}")
    print("Now ALL 'Pozitif' topics are green. Refresh the dashboard.")

if __name__ == "__main__":
    fix_all_duplicates()
