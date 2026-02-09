
from coaching.models import StudentProgress, Student

print("--- GLOBAL PROGRESS AUDIT (FIXED) ---")
all_sp = StudentProgress.objects.all()
print(f"Total Progress Records: {all_sp.count()}")

students = Student.objects.all()
for s in students:
    p_count = StudentProgress.objects.filter(student=s).count()
    done_count = StudentProgress.objects.filter(student=s, is_completed=True).count()
    if p_count > 0:
        print(f"Student ID: {s.id} | Name: {s.full_name} | Total Records: {p_count} | Completed: {done_count}")

print("\n--- RECENT ACTIVITY (TOP 10) ---")
recent = StudentProgress.objects.all().order_by('-updated_at')[:10]
for r in recent:
    print(f" - [{r.updated_at}] Student: {r.student_id} | Topic: {r.topic.title} | Done: {r.is_completed}")
