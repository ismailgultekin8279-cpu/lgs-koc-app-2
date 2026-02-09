
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def list_september_math():
    print("=== SEPTEMBER MATH TOPICS ===\n")
    math = Subject.objects.get(slug="matematik")
    topics = Topic.objects.filter(subject=math, month=9).order_by('week', 'order')
    
    for t in topics:
        print(f"ID: {t.id} | Week: {t.week} | Order: {t.order} | Title: {t.title}")

if __name__ == "__main__":
    list_september_math()
