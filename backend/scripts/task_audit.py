
from students.models import Student, StudyTask
from django.contrib.auth.models import User

print("--- TASK OWNERSHIP AUDIT ---")
# Get our target user
u = User.objects.get(username='iso')
s_linked = u.student_profile
print(f"User 'iso' is linked to Student ID {s_linked.id} ('{s_linked.full_name}')")

# Check tasks for today or generally
tasks = StudyTask.objects.all()
print(f"Total Tasks in DB: {tasks.count()}")

# Group tasks by student
from django.db.models import Count
by_student = StudyTask.objects.values('student', 'student__full_name').annotate(count=Count('id'))
for b in by_student:
    print(f"Student ID: {b['student']} ('{b['student__full_name']}') -> {b['count']} tasks.")

print("\n--- RECENTLY CLICKED TOPIC STATUS ---")
from coaching.models import StudentProgress
print(f"Checking Topic 1 status for ID {s_linked.id}:")
sp10 = StudentProgress.objects.filter(student_id=s_linked.id, topic_id=1).first()
if sp10: print(f" - ID 10: Topic 1 is_completed={sp10.is_completed}")
else: print(" - ID 10: No record found.")

print(f"Checking Topic 1 status for ID 1:")
sp1 = StudentProgress.objects.filter(student_id=1, topic_id=1).first()
if sp1: print(f" - ID 1: Topic 1 is_completed={sp1.is_completed}")
else: print(" - ID 1: No record found.")
