
from students.models import Student, StudyTask, Session, ExamResult, TopicPerformance
from coaching.models import StudentProgress
from django.db import transaction, connection

src_id = 1
dst_id = 10

print(f"--- MERGING STUDENT {src_id} -> {dst_id} ---")

with transaction.atomic():
    # 1. Update StudyTasks
    t_count = StudyTask.objects.filter(student_id=src_id).update(student_id=dst_id)
    print(f"Migrated {t_count} StudyTasks.")
    
    # 2. Update Sessions
    s_count = Session.objects.filter(student_id=src_id).update(student_id=dst_id)
    print(f"Migrated {s_count} Sessions.")

    # 3. Update StudentProgress
    # Need to handle potential duplicates for unique_together
    sp_src = StudentProgress.objects.filter(student_id=src_id)
    migrated_sp = 0
    for sp in sp_src:
        # Check if dst already has this topic
        if not StudentProgress.objects.filter(student_id=dst_id, topic_id=sp.topic_id).exists():
            sp.student_id = dst_id
            sp.save()
            migrated_sp += 1
        else:
            # If both exist, merge status (if either is done, dst is done)
            if sp.is_completed:
                StudentProgress.objects.filter(student_id=dst_id, topic_id=sp.topic_id).update(
                    is_completed=True,
                    completed_at=sp.completed_at or timezone.now()
                )
            sp.delete()
    print(f"Migrated/Merged {migrated_sp} StudentProgress records.")

    # 4. Update ExamResults (if any)
    e_count = ExamResult.objects.filter(student_id=src_id).update(student_id=dst_id)
    print(f"Migrated {e_count} ExamResults.")

    # 5. Delete Student 1
    Student.objects.filter(id=src_id).delete()
    print(f"Deleted Student ID {src_id}.")

connection.close()
print("--- MERGE COMPLETE ---")
