
from coaching.models import Topic, Subject, Student
from coaching.models import StudentProgress
from django.db.models import Exists, OuterRef

print("--- DEBUGGING API QUERY LOGIC ---")

try:
    student = Student.objects.get(id=10)
    print(f"Goal Student: {student.full_name} (ID: 10)")
except:
    print("Student 10 not found (CRITICAL)")
    exit()

subject = Subject.objects.get(name__iexact="Matematik")
print(f"Goal Subject: {subject.name}")

# Replicating views.py logic exactly
topics = Topic.objects.filter(subject=subject, id=1) # Target Topic 1 specificially

is_completed_subquery = StudentProgress.objects.filter(
    student=student,
    topic=OuterRef('pk'),
    is_completed=True
)
topics = topics.annotate(is_completed=Exists(is_completed_subquery))

print(f"Running Query for Topic 1...")
for t in topics:
    print(f"Topic: {t.title} (ID: {t.id})")
    print(f"  -> ANNOTATED is_completed: {t.is_completed}")

    # Manual check to verify verify
    manual_exists = StudentProgress.objects.filter(student=student, topic=t, is_completed=True).exists()
    print(f"  -> MANUAL CHECK: {manual_exists}")
