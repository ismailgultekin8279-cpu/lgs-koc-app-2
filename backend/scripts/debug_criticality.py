import os
import django
import sys

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, ExamResult
from coaching.services import CoachingService

def debug_criticality():
    student = Student.objects.get(id=10)
    service = CoachingService(student)
    
    latest_exams = ExamResult.objects.filter(student_id=student.id).order_by('-exam_date', '-id')
    latest_date = latest_exams.first().exam_date
    todays_results = latest_exams.filter(exam_date=latest_date).order_by('-id')
    
    print(f"Latest Exam Date: {latest_date}")
    weights = {"Matematik": 4.0, "Fen Bilimleri": 4.0, "Türkçe": 4.0, "T.C. İnkılap Tarihi": 2.0, "Yabancı Dil": 2.0, "Din Kültürü": 2.0}
    
    results_to_sort = []
    seen = set()
    for e in todays_results:
        if e.subject in seen: continue
        seen.add(e.subject)
        
        total = e.correct + e.wrong + e.blank
        rate = e.correct / total if total > 0 else 0
        coeff = 2.0
        for k, v in weights.items():
            if k.lower() in e.subject.lower() or e.subject.lower() in k.lower():
                coeff = v
                break
        score = (1.0 - rate) * coeff
        results_to_sort.append({'subj': e.subject, 'rate': rate, 'coeff': coeff, 'score': score})
        print(f"Subj: {e.subject}, Rate: {rate:.2f}, Coeff: {coeff}, Score: {score:.2f}")

    results_to_sort.sort(key=lambda x: x['score'], reverse=True)
    print("\nFinal Sorted Order:")
    for r in results_to_sort:
        print(f" -> {r['subj']} (Score: {r['score']:.2f})")

if __name__ == "__main__":
    debug_criticality()
