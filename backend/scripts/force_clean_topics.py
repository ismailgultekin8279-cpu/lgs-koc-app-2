
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic

corrections = [
    # Math
    {"sub": "Matematik", "order": 0, "title": "Pozitif Tam Sayıların Çarpanları"},
    {"sub": "Matematik", "order": 1, "title": "Asal Çarpanlara Ayırma"},
    {"sub": "Matematik", "order": 10, "title": "Temel İşlem Yeteneği"},
    {"sub": "Matematik", "order": 11, "title": "Mantık Muhakeme (Giriş)"},
    {"sub": "Matematik", "order": 12, "title": "Sayısal Analiz Becerisi"},
    {"sub": "Matematik", "order": 13, "title": "Problem Çözme Stratejileri"},
    {"sub": "Matematik", "order": 14, "title": "İşlem Hızı Geliştirme"},
    # Turkish
    {"sub": "Türkçe", "order": 10, "title": "Paragraf Yorumlama (Giriş)"},
    # Science
    {"sub": "Fen Bilimleri", "order": 10, "title": "Bilimsel Süreç Becerileri"},
    # Guidance
    {"sub": "Rehberlik", "order": 1, "title": "Dikkat ve Odaklanma"},
]

print("Force updating Week 1 topics with clean titles...")

for item in corrections:
    sub, _ = Subject.objects.get_or_create(name=item["sub"])
    Topic.objects.update_or_create(
        subject=sub,
        month=9,
        week=1,
        order=item["order"],
        defaults={"title": item["title"]}
    )
    print(f"Updated/Verified: {item['sub']} (Order {item['order']}) -> {item['title']}")

print("All Week 1 topics are now clean.")
