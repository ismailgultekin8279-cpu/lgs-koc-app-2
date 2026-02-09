
from django.contrib.auth.models import User
from students.models import Student

print("--- USER / STUDENT MAPPING ---")
users = User.objects.all()
for u in users:
    try:
        s = u.student_profile
        print(f"User: {u.username} (ID: {u.id}) -> Student: {s.full_name} (ID: {s.id})")
    except Exception as e:
        print(f"User: {u.username} (ID: {u.id}) -> NO STUDENT PROFILE ({e})")

print("\n--- ALL STUDENTS ---")
students = Student.objects.all()
for s in students:
    print(f"Student: {s.full_name} (ID: {s.id})")
