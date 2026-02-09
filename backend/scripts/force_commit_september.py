
from coaching.models import StudentProgress, Topic
from django.db import transaction, connection

sid = 10
print(f"--- NUCLEAR SEPTEMBER COMMIT FOR STUDENT {sid} ---")

# Math Month 9 topics
topics = Topic.objects.filter(subject__name__iexact="Matematik", month=9)
topic_ids = list(topics.values_list('id', flat=True))

print(f"Topics to complete ({len(topic_ids)}): {topic_ids}")

with transaction.atomic():
    for tid in topic_ids:
        sp, created = StudentProgress.objects.get_or_create(student_id=sid, topic_id=tid)
        sp.is_completed = True
        sp.save()
    print("Updates saved in transaction.")

connection.close()
print("Connection flushed. All September Math topics should be COMPLETE.")
