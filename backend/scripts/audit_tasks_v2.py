
from students.models import Student, StudyTask
from django.db.models import Count

sid = 10
print(f"--- TASK AUDIT FOR STUDENT {sid} ---")
s = Student.objects.get(id=sid)
tasks = StudyTask.objects.filter(student=s)
print(f"Student: {s.full_name}")
print(f"Task Count: {tasks.count()}")

for t in tasks:
    print(f" - ID: {t.id} | Date: {t.date} | Subject: {t.subject} | Topic: {t.topic_name} | Status: {t.status}")

# Check for any tasks left for ID 1 (should be 0)
print(f"\nTasks for ID 1: {StudyTask.objects.filter(student_id=1).count()}")
