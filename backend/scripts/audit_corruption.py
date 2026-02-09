
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

def audit():
    print("--- Week 1 ---")
    w1 = Topic.objects.filter(month=9, week=1).order_by('order')
    for t in w1:
        print(f"ID: {t.id} | Order: {t.order} | Subject: {t.subject.name} | Title: {t.title}")

    print("\n--- Week 2 ---")
    w2 = Topic.objects.filter(month=9, week=2).order_by('order')
    for t in w2:
        print(f"ID: {t.id} | Order: {t.order} | Subject: {t.subject.name} | Title: {t.title}")

audit()
