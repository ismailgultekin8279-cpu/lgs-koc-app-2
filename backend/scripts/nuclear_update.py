
from coaching.models import StudentProgress

print("--- NUCLEAR UPDATE ON ID 34 ---")
count = StudentProgress.objects.filter(id=34).update(is_completed=True)
print(f"Updated {count} rows.")

sp = StudentProgress.objects.get(id=34)
print(f"Verification: ID={sp.id}, IsCompleted={sp.is_completed}")
