
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

parens = Topic.objects.filter(title__contains='(')
print(f"Count: {parens.count()}")
for t in parens:
    print(t.title)
