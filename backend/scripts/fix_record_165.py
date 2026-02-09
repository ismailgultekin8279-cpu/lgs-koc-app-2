
import os
import django
import sys
from django.utils import timezone

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import StudentProgress

print("=== ULTRA SURGICAL FIX: RECORD ID 165 ===\n")

# Get the exact record
record = StudentProgress.objects.get(id=165)

print(f"BEFORE:")
print(f"  Is Completed: {record.is_completed}")
print(f"  Completed At: {record.completed_at}\n")

# Force update
record.is_completed = True
record.completed_at = timezone.now()
record.save()

# Verify
record.refresh_from_db()

print(f"AFTER:")
print(f"  Is Completed: {record.is_completed}")
print(f"  Completed At: {record.completed_at}\n")

if record.is_completed:
    print("✅✅✅ SUCCESS! Record 165 is now COMPLETED!")
else:
    print("❌❌❌ FAILED!")
