
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject

def check_subjects():
    print("=== SUBJECTS ENCODING AUDIT ===\n")
    for s in Subject.objects.all():
        print(f"ID: {s.id} | Slug: {s.slug} | Name: {s.name}")
        print(f"  Hex: {s.name.encode('utf-8').hex()}")
        print("-" * 20)

if __name__ == "__main__":
    check_subjects()
