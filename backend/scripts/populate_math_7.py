
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic

# We need 3 more Math topics to reach 7 (2 Core + 2 existing Extras + 3 New = 7)
new_extras = [
    {"subject": "Matematik", "title": "Sayısal Analiz Becerisi", "month": 9, "week": 1, "order": 12},
    {"subject": "Matematik", "title": "Problem Çözme Stratejileri", "month": 9, "week": 1, "order": 13},
    {"subject": "Matematik", "title": "İşlem Hızı Geliştirme", "month": 9, "week": 1, "order": 14},
]

print("Adding 3 More Math Topics for Week 1 (Total -> 7)...")

sub = Subject.objects.get(name="Matematik")

for item in new_extras:
    t, created = Topic.objects.get_or_create(
        subject=sub,
        title=item["title"],
        month=item["month"],
        week=item["week"],
        defaults={"order": item["order"]}
    )
    if created:
        print(f"Created: {item['title']}")
    else:
        print(f"Exists: {item['title']}")

print("Done. Math Week 1 should now have 7 topics.")
