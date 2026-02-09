
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic

def summarize_curriculum():
    print("=== CURRICULUM SUMMARY ===")
    for s in Subject.objects.all():
        topics = Topic.objects.filter(subject=s)
        months = topics.values_list('month', flat=True).distinct()
        print(f"Subject: {s.name} ({s.slug})")
        print(f"  Total Topics: {topics.count()}")
        print(f"  Months covered: {list(months)}")
        
        # Check for weird weeks
        weeks = topics.values_list('week', flat=True).distinct()
        print(f"  Weeks covered: {list(weeks)}")
        
        if None in months or None in weeks:
            print("  !!! WARNING: Contains NULL months or weeks !!!")
        
        print("-" * 20)

if __name__ == "__main__":
    summarize_curriculum()
