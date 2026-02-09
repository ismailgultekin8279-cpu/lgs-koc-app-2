
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.services import CoachingService

print("=== FINAL FORCE REGENERATION ===\n")

# Get student
student = Student.objects.get(id=10)
print(f"Student: {student.full_name}")
print(f"Student ID: {student.id}\n")

# Delete ALL existing tasks for this student to force clean slate
deleted_count, _ = StudyTask.objects.filter(student=student).delete()
print(f"Deleted {deleted_count} old tasks\n")

# Generate fresh plan
print("Generating new plan with FIXED code...\n")
service = CoachingService(student)
tasks = service.generate_daily_plan()

print(f"✅ Generated {len(tasks)} tasks\n")

# Show first 5 tasks
print("First 5 tasks:")
for i, task in enumerate(tasks[:5], 1):
    print(f"{i}. {task.subject} - {task.topic_name}")
    print(f"   Topic ID: {task.topic_id}, Status: {task.status}\n")

# Critical checks
pozitif_count = sum(1 for t in tasks if 'pozitif' in t.topic_name.lower())
asal_count = sum(1 for t in tasks if 'asal' in t.topic_name.lower())

print("\n=== VERIFICATION ===")
print(f"Pozitif in plan: {pozitif_count} tasks")
print(f"Asal in plan: {asal_count} tasks\n")

if pozitif_count == 0:
    print("✅✅✅ SUCCESS! POZITIF REMOVED FROM PLAN!")
else:
    print("❌❌❌ FAILED! POZITIF STILL IN PLAN!")

if asal_count > 0:
    print("✅✅✅ SUCCESS! ASAL ÇARPANLAR IN PLAN!")
else:
    print("⚠️ Asal not in plan yet")
