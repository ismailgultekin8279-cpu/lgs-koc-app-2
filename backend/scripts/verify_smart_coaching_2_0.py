import os
import django
import sys

# Setup Django
sys.path.append(r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, ExamResult, StudyTask
from coaching.ai_service import AICoachingService
from datetime import date, timedelta

def verify_smart_coaching():
    student_id = 10
    student = Student.objects.get(id=student_id)
    service = AICoachingService(student)
    
    print(f"--- Smart Coaching 2.0 Audit for {student.full_name} ---")
    
    # 1. Check/Seed Exam Results for testing
    print("\n[Step 1] Checking Exam Results...")
    if not ExamResult.objects.filter(student_id=student_id).exists():
        print("Seeding dummy exam results (Bad Math, Good Science)...")
        today = date.today()
        # Bad Math (low net)
        ExamResult.objects.create(student_id=student_id, exam_date=today - timedelta(days=7), subject="Matematik", net=2, correct=3, wrong=10)
        # Good Science (high net)
        ExamResult.objects.create(student_id=student_id, exam_date=today - timedelta(days=7), subject="Fen Bilimleri", net=18, correct=18, wrong=2)
    
    # 2. Check Weights
    print("\n[Step 2] Calculating Weights...")
    weights = service._calculate_subject_weights()
    for subj, w in weights.items():
        print(f"  {subj}: {w:.2f}")
    
    if weights.get("Matematik", 0) > weights.get("Fen Bilimleri", 0):
        print("✅ SUCCESS: Math has higher weight due to low exam score.")
    else:
        print("❌ FAILURE: Math should have higher weight.")

    # 3. Generate Plan (Fallback mode if no API key)
    print("\n[Step 3] Generating 7-Day Plan...")
    plan_tasks = service._generate_fallback_response({}, date.today())
    
    # 4. Analyze Distribution
    print("\n[Step 4] Analyzing Distribution...")
    days = {}
    for task in plan_tasks:
        d = task.date
        if d not in days: days[d] = []
        days[d].append(task)
        
    for d, tasks in sorted(days.items()):
        day_name = d.strftime('%A')
        print(f"\n{day_name} ({d}):")
        for t in tasks:
            print(f"  - [{t.subject}] {t.topic_name} ({t.task_type})")
            
        # Check Rules
        if day_name == 'Saturday':
             if any(t.subject == "Deneme Sınavı" for t in tasks):
                 print("  ✅ Match: Saturday is Mock Exam day.")
             else:
                 print("  ❌ Fail: Saturday missing Mock Exam.")
        elif day_name == 'Sunday':
             if any(t.subject == "Genel Tekrar" for t in tasks):
                 print("  ✅ Match: Sunday is Recovery day.")
             else:
                 print("  ❌ Fail: Sunday missing Recovery.")
        else:
            if len(tasks) == 3:
                print("  ✅ Match: 3 lessons (2+1) layout.")
            else:
                print(f"  ❌ Fail: Expected 3 lessons, got {len(tasks)}.")

if __name__ == "__main__":
    verify_smart_coaching()
