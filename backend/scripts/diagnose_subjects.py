
import os
import django
import sys

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic, StudentProgress
from students.models import Student

def diagnose_curriculum():
    print("=== Subject Audit ===")
    subjects = Subject.objects.all()
    for s in subjects:
        print(f"ID: {s.id}, Name: {s.name}, Slug: {s.slug}")
    
    slugs = subjects.values_list('slug', flat=True)
    if len(slugs) != len(set(slugs)):
        print("!!! ERROR: Duplicate slugs found !!!")
        from collections import Counter
        counts = Counter(slugs)
        for slug, count in counts.items():
            if count > 1:
                print(f"Duplicate slug: '{slug}' ({count} times)")
    
    print("\n=== Student 10 Audit ===")
    try:
        student = Student.objects.get(id=10)
        print(f"Student: {student.full_name}, User: {student.user.username if student.user else 'None'}")
    except Student.DoesNotExist:
        print("Student 10 not found!")

    print("\n=== Curriculum Tree Test ===")
    subject_slug = 'matematik'
    try:
        subject = Subject.objects.get(slug=subject_slug)
        topics = Topic.objects.filter(subject=subject).count()
        print(f"Topcs for '{subject_slug}': {topics}")
    except Exception as e:
        print(f"Error fetching subject '{subject_slug}': {type(e).__name__} - {e}")

if __name__ == "__main__":
    diagnose_curriculum()
