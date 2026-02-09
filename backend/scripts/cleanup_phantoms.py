import os
import django
import sys
from datetime import date

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import ExamResult

def cleanup_phantom_fails():
    today = date.today()
    # Find results from today for student 10 where net is 0.00 (indicates phantom entry)
    # BUT we only delete if they match our 'phantom' signature (0 correct, 0 wrong)
    phantoms = ExamResult.objects.filter(
        student_id=10, 
        exam_date=today,
        correct=0,
        wrong=0,
        net=0
    )
    
    count = phantoms.count()
    if count > 0:
        print(f"Cleaning up {count} phantom fail(s) for today...")
        for p in phantoms:
            print(f"Deleting phantom fail: {p.subject} (Date: {p.exam_date})")
        phantoms.delete()
        print("Cleanup complete. 🧹✨")
    else:
        print("No phantom fails found for today. 👍")

if __name__ == "__main__":
    cleanup_phantom_fails()
