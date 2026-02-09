
import os
import django
import sys
from django.utils import timezone

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import StudentProgress, Topic
from students.models import Student

def nuclear_write():
    print("--- NUCLEAR WRITE ---")
    try:
        student = Student.objects.get(id=10)
        topic = Topic.objects.get(id=2430)
    except Exception as e:
        print(f"Error finding objects: {e}")
        return

    # 1. DELETE existing
    deleted_count, _ = StudentProgress.objects.filter(student=student, topic=topic).delete()
    print(f"Deleted {deleted_count} existing records.")

    # 2. CREATE fresh
    prog = StudentProgress.objects.create(
        student=student,
        topic=topic,
        is_completed=True,
        completed_at=timezone.now()
    )
    prog.save() # Double tap
    
    print(f"Created NEW record: ID {prog.id}, Completed: {prog.is_completed}")

    # 3. VERIFY immediately
    check = StudentProgress.objects.get(id=prog.id)
    print(f"Immediate Verification: {check.is_completed}")
    
    # 4. Check Total
    count = StudentProgress.objects.filter(student=student, is_completed=True).count()
    print(f"Total Completed for Student 10: {count}")

if __name__ == "__main__":
    nuclear_write()
