
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

# Known mojibake mappings
# These are common when UTF-8 bytes are interpreted as ISO-8859-1 or Windows-1254 and then saved
# Ä° -> İ, ÅŸ -> ş, Ã§ -> ç, Ã¶ -> ö, Ã¼ -> ü, ÄŸ -> ğ, Ä± -> ı
mapping = {
    "Ä°": "İ",
    "ÅŸ": "ş",
    "Ã§": "ç",
    "Ã¶": "ö",
    "Ã¼": "ü",
    "ÄŸ": "ğ",
    "Ä±": "ı",
    "Ã‡": "Ç",
    "Ä": "İ", # Catch-all for some variants
}

def fix_text(text):
    if not text: return text
    fixed = text
    # Order matters: replace longer/more specific sequences first
    for corrupted, clean in mapping.items():
        fixed = fixed.replace(corrupted, clean)
    return fixed

print("Starting encoding repair...")
topics = Topic.objects.filter(month=9, week=1)
for t in topics:
    new_title = fix_text(t.title)
    if new_title != t.title:
        old = t.title
        t.title = new_title
        t.save()
        print(f"Fixed: {old} -> {new_title}")

print("Encoding repair complete.")
