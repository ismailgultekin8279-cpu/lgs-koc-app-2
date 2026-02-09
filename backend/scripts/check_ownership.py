
from coaching.models import StudentProgress, Student

print("--- OWNER CHECK ---")
sp_ids = [34] # The one we've been hitting
for sid in sp_ids:
    try:
        sp = StudentProgress.objects.get(id=sid)
        print(f"Record ID {sid}: Student='{sp.student.full_name}' (ID: {sp.student.id}), Topic='{sp.topic.title}', IsCompleted={sp.is_completed}")
    except:
        print(f"Record ID {sid} not found.")

print("\n--- ALL COMPLETED RECORDS ---")
all_done = StudentProgress.objects.filter(is_completed=True)
print(f"Total Completed Records in DB: {all_done.count()}")
for d in all_done:
    print(f" - Student: {d.student.full_name} (ID: {d.student.id}) | Topic: {d.topic.title} (ID: {d.topic.id})")
