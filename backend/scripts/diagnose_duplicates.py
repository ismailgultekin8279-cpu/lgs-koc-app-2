
from coaching.models import StudentProgress, Student, Topic
from django.conf import settings
from django.db.models import Count

print(f"DB Path: {settings.DATABASES['default']['NAME']}")

sid = 10
tid = 1

print(f"--- CHECKING FOR DUPLICATES S:{sid} T:{tid} ---")
entries = StudentProgress.objects.filter(student_id=sid, topic_id=tid)
print(f"Count: {entries.count()}")
for e in entries:
    print(f" - ID: {e.id} | Completed: {e.is_completed} | Date: {e.completed_at}")

print("--- GLOBAL DUPLICATE CHECK ---")
dupes = StudentProgress.objects.values('student', 'topic').annotate(count=Count('id')).filter(count__gt=1)
if dupes.exists():
    print(f"WARNING: Found {dupes.count()} duplicate groups!")
    for d in dupes:
        print(d)
else:
    print("No global duplicates found.")
