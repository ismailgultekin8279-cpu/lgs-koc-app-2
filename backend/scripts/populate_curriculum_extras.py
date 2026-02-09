
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic

# Ensure 'Rehberlik' subject exists
rehberlik, _ = Subject.objects.get_or_create(name="Rehberlik")

extras = [
    {"subject": "Matematik", "title": "Temel İşlem Yeteneği", "month": 9, "week": 1, "order": 10},
    {"subject": "Matematik", "title": "Mantık Muhakeme (Giriş)", "month": 9, "week": 1, "order": 11},
    {"subject": "Türkçe", "title": "Paragraf Yorumlama (Giriş)", "month": 9, "week": 1, "order": 10},
    {"subject": "Fen Bilimleri", "title": "Bilimsel Süreç Becerileri", "month": 9, "week": 1, "order": 10},
    {"subject": "Rehberlik", "title": "Dikkat ve Odaklanma", "month": 9, "week": 1, "order": 1},
]

print("Adding Supplemental Topics for Week 1...")

for item in extras:
    # Use get_or_create to be safe
    sub, _ = Subject.objects.get_or_create(name=item["subject"])
    t, created = Topic.objects.get_or_create(
        subject=sub,
        title=item["title"],
        month=item["month"],
        week=item["week"],
        defaults={"order": item["order"]}
    )
    if created:
        print(f"Created: {item['subject']} - {item['title']}")
    else:
        print(f"Exists: {item['subject']} - {item['title']}")

print("Done.")
