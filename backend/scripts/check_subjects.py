import os
import django
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject

def check_subjects():
    subjects = Subject.objects.all()
    print("Existing Subjects in DB:")
    for s in subjects:
        print(f"- '{s.name}' (Slug: {s.slug})")

    expected = ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "Din Kültürü", "Yabancı Dil"]
    print("\nVerifying Expected Subjects:")
    for name in expected:
        exists = Subject.objects.filter(name__iexact=name).exists()
        print(f"- {name}: {'FOUND' if exists else 'MISSING'}")

if __name__ == "__main__":
    check_subjects()
