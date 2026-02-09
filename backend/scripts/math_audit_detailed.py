
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

def full_audit():
    print("--- MATHEMATICS AUDIT (WEEKS 1-4) ---")
    for w in range(1, 5):
        print(f"\n[SEPTEMBER WEEK {w}]")
        topics = Topic.objects.filter(subject__name="Matematik", month=9, week=w).order_by('order')
        for t in topics:
            print(f"ID: {t.id} | Order: {t.order} | Title: {t.title}")

full_audit()
