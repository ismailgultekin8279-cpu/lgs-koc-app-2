
from coaching.models import StudentProgress, Topic
from students.models import Student

sid = 10
print(f"--- RESETTING SEPTEMBER MATH PROGRESS FOR STUDENT {sid} ---")

# Math Month 9 topics
topics = Topic.objects.filter(subject__name__iexact="Matematik", month=9)
topic_ids = list(topics.values_list('id', flat=True))

print(f"Topics to reset ({len(topic_ids)}): {topic_ids}")

count = StudentProgress.objects.filter(student_id=sid, topic_id__in=topic_ids).update(
    is_completed=False,
    completed_at=None
)

print(f"Reset {count} records to 'pending'.")
