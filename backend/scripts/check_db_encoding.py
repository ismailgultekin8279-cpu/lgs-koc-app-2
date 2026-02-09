
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic

def check_encoding():
    print("=== DATABASE ENCODING AUDIT ===\n")
    
    print("Checking Subjects:")
    for s in Subject.objects.all():
        print(f"ID: {s.id} | Name: {s.name} | Hex: {s.name.encode('utf-8').hex()}")
        
    print("\nChecking first few Topics:")
    for t in Topic.objects.all()[:10]:
        print(f"ID: {t.id} | Title: {t.title} | Hex: {t.title.encode('utf-8').hex()}")

    print("\nChecking 'Pozitif' Topics Specifically:")
    for t in Topic.objects.filter(title__icontains="Pozitif")[:5]:
        print(f"ID: {t.id} | Title: {t.title} | Hex: {t.title.encode('utf-8').hex()}")

if __name__ == "__main__":
    check_encoding()
