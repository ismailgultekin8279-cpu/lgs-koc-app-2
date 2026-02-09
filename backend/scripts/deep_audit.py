import os
import django
import sys

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, ExamResult
from coaching.ai_service import AICoachingService

def deep_audit():
    student = Student.objects.get(id=10)
    ai_svc = AICoachingService(student)
    
    print("--- SUBJECT WEIGHTS AUDIT ---")
    weights = ai_svc._calculate_subject_weights()
    for s, w in weights.items():
        print(f"Subject: {s:20} | Weight: {w:10.2f}")
    
    crit_threshold = 6.8
    criticals = ai_svc.get_critical_subjects(threshold=crit_threshold)
    print(f"\nCalculated Critical Subjects (Threshold {crit_threshold}): {criticals}")

    print("\n--- LATEST EXAM RESULTS (PER SUBJECT) ---")
    for subj in weights.keys():
        res = ExamResult.objects.filter(student_id=student.id, subject__icontains=subj).order_by('-exam_date', '-id').first()
        if res:
            print(f"Subject: {res.subject:20} | Net: {res.net:6.2f} | Date: {res.exam_date}")

if __name__ == "__main__":
    deep_audit()
