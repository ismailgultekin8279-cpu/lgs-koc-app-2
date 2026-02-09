
from coaching.models import Subject, Topic

print("--- SUBJECT INTEGRITY CHECK ---")
try:
    s_slug = Subject.objects.get(slug='matematik')
    print(f"Subject (via slug='matematik'): ID={s_slug.id}, Name='{s_slug.name}'")
except Exception as e:
    print(f"Error fetching by slug: {e}")

try:
    s_name = Subject.objects.get(name='Matematik')
    print(f"Subject (via name='Matematik'): ID={s_name.id}, Slug='{s_name.slug}'")
except Exception as e:
    print(f"Error fetching by name: {e}")

all_sub = Subject.objects.filter(name__icontains="Matematik")
print(f"Total 'Matematik' Subjects: {all_sub.count()}")
for s in all_sub:
    print(f" - ID: {s.id} | Name: {s.name} | Slug: {s.slug}")

print("--- TOPIC 1 CHECK ---")
try:
    t = Topic.objects.get(id=1)
    print(f"Topic 1: '{t.title}'")
    print(f"Topic 1 Subject ID: {t.subject_id}")
    print(f"Topic 1 Subject Name: {t.subject.name}")
except:
    print("Topic 1 not found.")
