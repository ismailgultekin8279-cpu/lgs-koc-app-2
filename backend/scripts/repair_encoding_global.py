
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

replaces = [
    ("\u00C4\u00B0", "\u0130"), # Ä° -> İ
    ("\u00C5\u017F", "\u015F"), # ÅŸ -> ş
    ("\u00C3\u2021", "\u00C7"), # Ã‡ -> Ç
    ("\u00C3\u00A7", "\u00E7"), # Ã§ -> ç
    ("\u00C3\u2013", "\u00D6"), # Ã– -> Ö
    ("\u00C3\u00B6", "\u00F6"), # Ã¶ -> ö
    ("\u00C3\u0153", "\u00DC"), # Ãœ -> Ü
    ("\u00C3\u00BC", "\u00FC"), # Ã¼ -> ü
    ("\u00C4\u011F", "\u011F"), # ÄŸ -> ğ
    ("\u00C4\u00B1", "\u0131"), # Ä± -> ı
]

def clean_text(text):
    if not text: return text
    new_text = text
    for corrupted, clean in replaces:
        new_text = new_text.replace(corrupted, clean)
    return new_text

print("Repairing all subjects (with merging)...")

from django.core.exceptions import ObjectDoesNotExist

subjects = list(Subject.objects.all())
for s in subjects:
    try:
        s.refresh_from_db()
    except ObjectDoesNotExist:
        continue

    new_name = clean_text(s.name)
    if new_name != s.name:
        existing = Subject.objects.filter(name=new_name).exclude(id=s.id).first()
        if existing:
            print(f"Merging Subject: {s.name} into existing {existing.name}")
            # Move all topics
            Topic.objects.filter(subject=s).update(subject=existing)
            # Delete corrupted subject
            s.delete()
        else:
            print(f"Renaming Subject: {s.name} -> {new_name}")
            s.name = new_name
            s.save()

print("Repairing all topics...")
topics = Topic.objects.all()
count = 0
for t in topics:
    new_title = clean_text(t.title)
    if new_title != t.title:
        t.title = new_title
        t.save()
        count += 1

print(f"Fixed {count} topics.")
print("Done.")
