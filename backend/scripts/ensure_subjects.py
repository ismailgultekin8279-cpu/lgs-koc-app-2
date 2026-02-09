import os
import django
import sys
from django.utils.text import slugify

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject

def ensure_subjects():
    subjects = ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "Din Kültürü", "Yabancı Dil"]
    
    print("Ensuring subjects exist...")
    for name in subjects:
        slug = slugify(name.replace('ı', 'i').replace('İ', 'I')) # Basic turkish slugify help
        if not slug:
            slug = name.lower().replace(' ', '-')
            
        obj, created = Subject.objects.get_or_create(
            name=name,
            defaults={"slug": slug}
        )
        if created:
            print(f"Created: {name}")
        else:
            print(f"Exists: {name}")

if __name__ == "__main__":
    ensure_subjects()
