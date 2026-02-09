
from coaching.models import StudentProgress, Student
from django.db.models import Count

print("--- GLOBAL PROGRESS AUDIT ---")
all_sp = StudentProgress.objects.all()
print(f"Total Progress Records in DB: {all_sp.count()}")

# Group by student
by_student = StudentProgress.objects.values('student', 'student__full_name').annotate(
    total=Count('id'),
    done=Count('id', filter=models.Q(is_completed=True))
)

from django.db import models # Ensure models is available for Q
for s in by_student:
    print(f"Student {s['student']} ({s['student__full_name']}): Total={s['total']}, Completed={s['done']}")

print("\n--- RECENTLY COMPLETED ---")
recent = StudentProgress.objects.filter(is_completed=True).order_by('-updated_at')[:10]
for r in recent:
    print(f" - [{r.updated_at}] Student {r.student_id} Topic: {r.topic.title}")
