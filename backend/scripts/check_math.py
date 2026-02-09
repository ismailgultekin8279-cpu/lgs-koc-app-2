
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

print('--- Week 1 Math Topics ---')
topics = Topic.objects.filter(month=9, week=1, subject__name='Matematik').order_by('order')
for t in topics:
    print(f"{t.order}: {t.title}")
