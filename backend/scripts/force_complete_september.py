
from coaching.models import Topic, StudentProgress, Student
from django.conf import settings

# Get the correct student for 'iso' (ismail gültekin)
try:
    student = Student.objects.get(id=10)
    print(f"Updates for Student: {student.full_name} (ID: {student.id})")
except Student.DoesNotExist:
    print("Student ID 10 not found! Trying fallback...")
    student = Student.objects.first()
    
    # Get topics for Math Month 9
    topics = Topic.objects.filter(subject__slug="matematik", month=9)
    print(f"Found {topics.count()} topics for Math Month 9.")
    
    for t in topics:
        sp, created = StudentProgress.objects.get_or_create(
            student=student,
            topic=t
        )
        sp.is_completed = True
        sp.save()
        print(f"  - FORCE SAVED '{t.title}' as True (Current: {sp.is_completed})")

print("Done. Please verify in Frontend.")
