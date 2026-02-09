
from coaching.models import StudentProgress
from django.db import transaction, connection

print("--- EXPLICIT COMMIT UPDATE ---")
with transaction.atomic():
    count = StudentProgress.objects.filter(id=34).update(is_completed=True)
    print(f"Update count in transaction: {count}")

# Force connection closing to ensure flush (SQLite specific)
connection.close()

print("Connection closed to force flush.")

# Reopen and check
sp = StudentProgress.objects.get(id=34)
print(f"Final Persistence Check: ID={sp.id}, IsCompleted={sp.is_completed}")
