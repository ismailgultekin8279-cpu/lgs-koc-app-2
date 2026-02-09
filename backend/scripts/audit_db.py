
from coaching.models import StudentProgress
from django.db import connection

sid = 10
print(f"--- DATABASE AUDIT FOR STUDENT {sid} ---")
all_p = StudentProgress.objects.filter(student_id=sid)
print(f"Total Progress Records: {all_p.count()}")

completed = all_p.filter(is_completed=True)
print(f"Completed Records: {completed.count()}")
for c in completed:
    print(f" - {c.topic.title} (ID:{c.topic.id}) CompletedAt: {c.completed_at}")

# Check for duplicates or orphaned subjects
from coaching.models import Topic
print("\n--- TOPIC COUNT CHECK ---")
print(f"Total Topics in DB: {Topic.objects.count()}")

# Force flush check
connection.close()
print("Connection flushed.")
