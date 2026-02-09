import os
import django
import sys
from datetime import date

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.ai_service import AICoachingService
from students.models import Student, StudyTask

def rotation_audit():
    student = Student.objects.get(id=10)
    svc = AICoachingService(student)
    
    print("Triggering 7-day plan generation...")
    today = date.today()
    context = {
        "student_name": student.full_name,
        "grade": student.grade,
        "target_score": student.target_score,
        "exam_group": "LGS",
        "weak_subjects": svc.get_critical_subjects(),
        "recent_exams_summary": [],
        "completed_tasks_summary": [],
        "student_id": student.id
    }
    svc.generate_plan(context=context, target_date=today)
    
    today = date.today()
    tasks = StudyTask.objects.filter(student=student, date__gte=today).order_by('date')
    
    current_date = None
    for t in tasks:
        if t.date != current_date:
            current_date = t.date
            print(f"\n--- {current_date} ---")
        print(f"[{t.subject}] {t.topic_name} ({t.status})")

if __name__ == "__main__":
    rotation_audit()
