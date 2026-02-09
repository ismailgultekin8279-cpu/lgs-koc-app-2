
import os
import django
import sys
from collections import defaultdict

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

def audit_topics():
    topics = Topic.objects.filter(month=9, week=1).select_related('subject')
    d = defaultdict(list)
    for t in topics:
        d[t.subject.name].append(t.title)
    
    with open('topic_dist.txt', 'w', encoding='utf-8') as f:
        for subj, titles in d.items():
            f.write(f"{subj}: {len(titles)} topics\n")
            for t in titles:
                f.write(f"  - {t}\n")

if __name__ == "__main__":
    audit_topics()
