
import os
import django
import sys
from collections import Counter

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic

def verify():
    topics = Topic.objects.all()
    titles = [t.title for t in topics]
    counts = Counter(titles)
    
    dupes = [title for title, count in counts.items() if count > 1]
    
    with open('curriculum_uniqueness_report.txt', 'w', encoding='utf-8') as f:
        f.write(f"Total Topics: {len(topics)}\n")
        f.write(f"Unique Titles: {len(counts)}\n")
        f.write(f"Duplicate Count: {len(dupes)}\n")
        
        if dupes:
            f.write("\nDUPLICATES FOUND:\n")
            for d in dupes[:10]:
                f.write(f"  - {d}\n")
        else:
            f.write("\nSUCCESS: All topic titles are globally unique!\n")
            
        f.write("\n--- Sample Progression (Matematik) ---\n")
        math_topics = Topic.objects.filter(subject__name='Matematik', month=9).order_by('week', 'order')
        for t in math_topics[:14]:
            f.write(f"  Week {t.week} Order {t.order}: {t.title}\n")

if __name__ == "__main__":
    verify()
