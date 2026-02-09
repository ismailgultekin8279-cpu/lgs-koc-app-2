
from coaching.models import Topic, Subject, Student, StudentProgress
from django.db.models import Exists, OuterRef

print("--- DEBUGGING API QUERY LOGIC v3 ---")
student = Student.objects.get(id=10)
subject_name = "Matematik"

# Replicating views.py logic exactly
topics = Topic.objects.filter(subject__name__iexact=subject_name, id=1) 
print(f"Initial Topics Count: {topics.count()}")

is_completed_subquery = StudentProgress.objects.filter(
    student=student,
    topic=OuterRef('pk'),
    is_completed=True
)
topics = topics.annotate(is_completed=Exists(is_completed_subquery))

for t in topics:
    print(f"Topic: {t.title} (ID: {t.id})")
    print(f"  -> ANNOTATED is_completed: {t.is_completed}")
    
    # Manual check
    manual = StudentProgress.objects.filter(student=student, topic=t, is_completed=True).exists()
    print(f"  -> MANUAL CHECK: {manual}")
