
from coaching.models import Topic
try:
    t = Topic.objects.get(id=1)
    print(f"Topic 1: '{t.title}' Subject: '{t.subject.name}'")
except:
    print("Topic 1 does not exist.")
