
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

# Map of corrupted substrings -> correct
# Based on screenshot: ÃÄŸ -> İş, ÄŸ -> ğ, Ã§ -> ç, etc.
# Actually, it's easier to just fetch by mostly matching title and FORCE updating string.

updates = [
    {"contains": "Temel", "new_title": "Temel İşlem Yeteneği"},
    {"contains": "Mant", "new_title": "Mantık Muhakeme (Giriş)"},
    {"contains": "Say",  "new_title": "Sayısal Analiz Becerisi"},
    {"contains": "Prob", "new_title": "Problem Çözme Stratejileri"},
    {"contains": "HÄ±z", "new_title": "İşlem Hızı Geliştirme"}, # Match corrupted logic if needed, or by Week 1/Math
    {"contains": "Hız",  "new_title": "İşlem Hızı Geliştirme"},
    {"contains": "Paragraf", "new_title": "Paragraf Yorumlama (Giriş)"},
    {"contains": "Bilimsel", "new_title": "Bilimsel Süreç Becerileri"},
    {"contains": "Dikkat", "new_title": "Dikkat ve Odaklanma"},
]

print("Fixing Encoding 1...")

# Filter for Week 1 topics to avoid false positives
week1_topics = Topic.objects.filter(month=9, week=1)

for t in week1_topics:
    for u in updates:
        if u["contains"] in t.title: # This might fail if corruption doesn't contain the clean substring
             # simpler: just update based on order/subject if possible, but title match is safer
             # Let's try to match the corrupted beginning if possible
             pass

# Better approach: Just update by Subject + Order since we set them recently
corrections_by_order = [
    # Math
    {"subject": "Matematik", "order": 10, "title": "Temel İşlem Yeteneği"},
    {"subject": "Matematik", "order": 11, "title": "Mantık Muhakeme (Giriş)"},
    {"subject": "Matematik", "order": 12, "title": "Sayısal Analiz Becerisi"},
    {"subject": "Matematik", "order": 13, "title": "Problem Çözme Stratejileri"},
    {"subject": "Matematik", "order": 14, "title": "İşlem Hızı Geliştirme"},
    # Others
    {"subject": "Türkçe", "order": 10, "title": "Paragraf Yorumlama (Giriş)"},
    {"subject": "Fen Bilimleri", "order": 10, "title": "Bilimsel Süreç Becerileri"},
    {"subject": "Rehberlik", "order": 1, "title": "Dikkat ve Odaklanma"},
]

print("Fixing Encoding by Order/Subject safely...")
for item in corrections_by_order:
    try:
        t = Topic.objects.get(subject__name=item["subject"], order=item["order"], month=9, week=1)
        old_title = t.title
        t.title = item["title"]
        t.save()
        print(f"Fixed: {old_title} -> {t.title}")
    except Topic.DoesNotExist:
        print(f"Skipped (Not Found): {item['title']}")
