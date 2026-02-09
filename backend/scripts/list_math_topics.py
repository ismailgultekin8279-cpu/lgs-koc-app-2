
from coaching.models import Topic
print("--- DUMPING MATH TOPICS ---")
topics = Topic.objects.filter(subject__name__iexact="Matematik")
print(f"Total Topics: {topics.count()}")
for t in topics:
    print(f"ID: {t.id} | Title: '{t.title}'")
print("--- END DUMP ---")
