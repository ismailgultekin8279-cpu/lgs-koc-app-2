import os
import django
import sys

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import ExamResult

def history_audit():
    results = ExamResult.objects.filter(student_id=10).order_by('-exam_date', '-id')[:20]
    print(f"{'Date':12} | {'Subject':20} | {'Net':6}")
    print("-" * 45)
    for r in results:
        print(f"{str(r.exam_date):12} | {r.subject:20} | {r.net:6.2f}")

if __name__ == "__main__":
    history_audit()
