import os
import django
import sys
from datetime import date

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, ExamResult
from coaching.services import CoachingService
from coaching.ai_service import AICoachingService

def verify_phase_18():
    student = Student.objects.get(id=10)
    print(f"Testing for Student: {student.full_name}")
    
    # Check current exam results in DB for date 2026-02-06
    exams = ExamResult.objects.filter(student_id=student.id, exam_date=date(2026, 2, 6))
    print(f"Exam Results for 2026-02-06: {exams.count()}")
    for e in exams:
        print(f"  {e.subject}: Net={e.net}, C={e.correct}, W={e.wrong}, B={e.blank}")

    # 1. Test Weakness Analysis
    service = CoachingService(student)
    # We need to manually simulate the analyze_weaknesses logic to see scores if we want, 
    # but let's just see what the method returns.
    weaknesses = service._analyze_weaknesses()
    print(f"Detected Weaknesses (Prioritized): {weaknesses}")
    
    # 2. Test Fallback Plan Generation
    ai_service = AICoachingService(student)
    target_date = date.today()
    tasks = ai_service._generate_fallback_response({}, target_date)
    
    # Reload config to check message
    from coaching.models import CoachingConfig
    config = CoachingConfig.objects.get(student=student)
    print(f"Stored Coach Message: {config.last_coach_message}")
    
    # Check tasks for remediation
    remediation_tasks = [t for t in tasks if t.task_type == 'remediation']
    print(f"Found {len(remediation_tasks)} remediation tasks.")
    for t in remediation_tasks[:3]:
        print(f"  Task: {t.subject} - {t.topic_name}")

if __name__ == "__main__":
    verify_phase_18()
