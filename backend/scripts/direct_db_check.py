
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import StudentProgress, Topic
from students.models import Student

print("=== DIRECT DATABASE CHECK: TOPIC 2430 ===\n")

student = Student.objects.get(id=10)
topic = Topic.objects.get(id=2430)

print(f"Student: {student.full_name}")
print(f"Topic: {topic.title}\n")

# Check ALL StudentProgress records for this topic and student
all_records = StudentProgress.objects.filter(student=student, topic=topic)

print(f"Total records found: {all_records.count()}\n")

for record in all_records:
    print(f"Record ID: {record.id}")
    print(f"Is Completed: {record.is_completed}")
    print(f"Completed At: {record.completed_at}")
    print(f"Created: {record.id}")
    print()

# Check if ANY completed records exist for student 10
total_completed = StudentProgress.objects.filter(
    student=student,
    is_completed=True
).count()

print(f"Total COMPLETED records for student 10: {total_completed}")
