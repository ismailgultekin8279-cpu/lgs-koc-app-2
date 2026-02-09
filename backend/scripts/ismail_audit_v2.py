
from students.models import Student
from django.contrib.auth.models import User
from coaching.models import StudentProgress

print("--- ISMAIL AUDIT (FIXED) ---")
ismails = Student.objects.filter(full_name__icontains="ismail")
for s in ismails:
    user_str = "NONE"
    # Check User -> Student_profile
    linked_user = User.objects.filter(student_profile=s).first()
    if linked_user:
        user_str = f"{linked_user.username} (ID: {linked_user.id})"

    comp = StudentProgress.objects.filter(student=s, is_completed=True).count()
    total = StudentProgress.objects.filter(student=s).count()
    print(f"Student ID: {s.id} | Name: '{s.full_name}' | User: {user_str} | Progress: {comp}/{total}")

print("\n--- RECENT COMPLETED RECORDS (ANY STUDENT) ---")
recent = StudentProgress.objects.filter(is_completed=True).order_by('-updated_at')[:5]
for r in recent:
    try:
        print(f" - [{r.updated_at}] Student: {r.student_id} ({r.student.full_name}) Topic: {r.topic.title}")
    except:
        print(f" - [{r.updated_at}] Student: {r.student_id} (ORPHAN) Topic ID: {r.topic_id}")
