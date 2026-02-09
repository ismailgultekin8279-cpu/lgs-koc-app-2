
from coaching.models import StudentProgress, Student, Topic

sid = 10
tid = 1

print(f"--- CHECKING PROGRESS FOR S:{sid} T:{tid} ---")

try:
    sp = StudentProgress.objects.get(student_id=sid, topic_id=tid)
    print(f"FOUND: ID={sp.id}, IsCompleted={sp.is_completed}")
except StudentProgress.DoesNotExist:
    print("NOT FOUND! The entry does not exist.")

print(f"--- CHECKING ALL PROGRESS FOR STUDENT {sid} ---")
all_p = StudentProgress.objects.filter(student_id=sid)
print(f"Total entries: {all_p.count()}")
for p in all_p:
    print(f" - Topic: {p.topic.title} (ID:{p.topic.id}) -> {p.is_completed}")
