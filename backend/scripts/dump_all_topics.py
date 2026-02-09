
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

subjects = ['Fen Bilimleri', 'Din Kültürü', 'Yabancı Dil', 'T.C. İnkılap Tarihi', 'Türkçe', 'Matematik']
for s_name in subjects:
    print(f"\n[{s_name}]")
    topics = Topic.objects.filter(subject__name=s_name).order_by('month', 'week', 'order')
    for t in topics:
        print(f"  - M{t.month} W{t.week}: {t.title}")
