
import os
import django
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.ai_service import AICoachingService

try:
    student = Student.objects.get(id=10)
    service = AICoachingService(student)
    print(f"Generating plan for {student.full_name}...")
    
    # Mock context
    context = {
        "weaknesses": ["Matematik"],
        "curriculum_status": "Month 9, Week 1",
        "recent_exams": []
    }
    
    today = date.today()
    res = service._generate_fallback_response(context, today)
    print("Plan generated successfully!")
    
    # res is a list of StudyTask objects
    today_tasks = [t for t in res if t.date == today]
    print(f"Tasks count for today: {len(today_tasks)}")
    for t in sorted(today_tasks, key=lambda x: x.order):
        print(f" - {t.order}. {t.subject}: {t.topic_name}")

except Exception as e:
    import traceback
    print("CAUGHT ERROR:")
    traceback.print_exc()
