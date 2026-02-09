
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student
from coaching.services import CoachingService

def regenerate_plan():
    print("=== REGENERATE PLAN ===\n")
    
    try:
        student = Student.objects.get(id=10)
    except:
        print("❌ Student 10 not found")
        return
    
    print(f"Student: {student.full_name}\n")
    
    # Create service and generate
    service = CoachingService(student)
    
    print("Generating new plan...\n")
    tasks = service.generate_daily_plan()
    
    print(f"✅ Generated {len(tasks)} tasks for today ({date.today()})\n")
    
    # Show the tasks
    for i, task in enumerate(tasks, 1):
        print(f"{i}. {task.subject} - {task.topic_name}")
        print(f"   Topic ID: {task.topic_id}, Status: {task.status}\n")
    
    # Check if Pozitif is gone
    pozitif_tasks = [t for t in tasks if "pozitif" in t.topic_name.lower()]
    
    if pozitif_tasks:
        print("⚠️  POZITIF STILL IN NEW PLAN!")
    else:
        print("✅ POZITIF NOT IN NEW PLAN!")
        
        # Check if Asal is there
        asal_tasks = [t for t in tasks if "asal" in t.topic_name.lower()]
        if asal_tasks:
            print("✅ ASAL ÇARPANLAR IS IN THE PLAN!")

if __name__ == "__main__":
    regenerate_plan()
