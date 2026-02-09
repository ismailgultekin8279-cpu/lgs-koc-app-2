
from students.models import Student, StudyTask
from coaching.models import StudentProgress
from django.utils import timezone

src_id = 1
dst_id = 10

print("--- BULK MERGE START ---")

# 1. Update StudyTasks
StudyTask.objects.filter(student_id=src_id).update(student_id=dst_id)
print("Tasks migrated.")

# 2. Handle Progress (Atomic enough for this purpose)
src_done_ids = list(StudentProgress.objects.filter(student_id=src_id, is_completed=True).values_list('topic_id', flat=True))
print(f"IDs to carry over from 1 to 10: {src_done_ids}")

for tid in src_done_ids:
    sp, created = StudentProgress.objects.get_or_create(student_id=dst_id, topic_id=tid)
    sp.is_completed = True
    sp.save()

# 3. Final Cleanup
StudentProgress.objects.filter(student_id=src_id).delete()
Student.objects.filter(id=src_id).delete()
print("Cleanup done.")

# Check final state
print(f"Final Count for ID 10: {StudentProgress.objects.filter(student_id=10, is_completed=True).count()}")
