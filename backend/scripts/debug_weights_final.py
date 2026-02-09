import os
import django
import sys
import json

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.ai_service import AICoachingService

def debug_weights():
    student = Student.objects.get(id=10)
    service = AICoachingService(student)
    
    weights = service._calculate_subject_weights()
    print("Subject Weights:")
    for s, w in weights.items():
        print(f" - {s}: {w}")
        
    m, w, week_topics = service._get_academic_week_scope()
    print(f"\nAcademic Week: {m} Month, Week {w}")
    
    # Check top weakness detection logic
    crit_threshold = 5.5
    critical_subjects = [s for s, w in weights.items() if w > crit_threshold]
    critical_subjects.sort(key=lambda s: weights[s], reverse=True)
    
    print(f"\nCritical Subjects (Threshold {crit_threshold}): {critical_subjects}")
    if critical_subjects:
        top_weakness = critical_subjects[0]
        print(f"Top Weakness: {top_weakness}")

if __name__ == "__main__":
    debug_weights()
