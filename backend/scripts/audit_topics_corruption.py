
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, Subject

def audit_topics():
    print("=== TOPICS CORRUPTION AUDIT ===\n")
    
    valid_subject_ids = [1, 2, 3, 4, 5, 6]
    
    corrupted_topics = Topic.objects.exclude(subject_id__in=valid_subject_ids)
    print(f"Topics with invalid Subject IDs: {corrupted_topics.count()}")
    for t in corrupted_topics[:20]:
        print(f"ID: {t.id} | SubID: {t.subject_id} | Title: {t.title}")
        
    print("\nChecking for duplicate titles in valid subjects (Matematik ID: 1):")
    from django.db.models import Count
    dupes = Topic.objects.filter(subject_id=1).values('title').annotate(count=Count('id')).filter(count__gt=1)
    print(f"Duplicate titles in Matematik: {len(dupes)}")
    for d in dupes[:10]:
        print(f"Title: {d['title']} | Count: {d['count']}")

if __name__ == "__main__":
    audit_topics()
