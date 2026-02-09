
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

def full_year_audit():
    months = [10, 11, 12, 1, 2, 3, 4, 5, 6]
    print("--- GLOBAL MATHEMATICS AUDIT (OCT-JUN) ---")
    for m in months:
        print(f"\n[MONTH {m}]")
        for w in range(1, 5):
            topics = Topic.objects.filter(subject__name="Matematik", month=m, week=w).order_by('order')
            if topics.exists():
                print(f"  Week {w}: {topics.count()} topics")
                for t in topics[:3]: # Just show first 3 to see names
                    print(f"    - {t.title}")
            else:
                print(f"  Week {w}: EMPTY")

full_year_audit()
