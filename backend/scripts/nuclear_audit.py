
import os
import django
import json
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic, StudentProgress, CoachingConfig
from students.models import Student, StudyTask

def nuclear_audit():
    sid = 10
    student = Student.objects.get(id=sid)
    config = student.coaching_config
    
    print(f"--- NUCLEAR AUDIT: Student {sid} ({student.full_name}) ---")
    print(f"Config: Month {config.current_academic_month}, Week {config.current_academic_week}, Started {config.week_started_at}")
    
    # 1. Total Topics in Month 9 Week 1
    m, w = 9, 1
    topics = Topic.objects.filter(month=m, week=w)
    print(f"\nTopics in M{m}W{w}: {topics.count()}")
    
    # 2. Progress for these topics
    progs = StudentProgress.objects.filter(student=student, topic__in=topics)
    print(f"Progress records found: {progs.count()}")
    for p in progs:
        print(f"  Topic {p.topic.id} ({p.topic.title}): {p.is_completed}")
        
    # 3. StudyTasks for today
    today = date.today()
    tasks = StudyTask.objects.filter(student=student, date=today)
    print(f"\nTasks for today ({today}): {tasks.count()}")
    for t in tasks:
        print(f"  Task {t.id}: {t.topic_name} (ID: {t.topic_id}) status: {t.status}")

    # 4. Check for duplicates (Multiple subjects/topics with same name)
    dupe_subjects = Subject.objects.filter(name__icontains="Matematik")
    print(f"\nMatematik Subjects: {dupe_subjects.count()}")
    for s in dupe_subjects:
        print(f"  ID: {s.id}, Name: {repr(s.name)}, Slug: {s.slug}")

    # 5. Check topic 2430 specifically
    try:
        t2430 = Topic.objects.get(id=2430)
        print(f"\nTopic 2430: {t2430.title}, M:{t2430.month}, W:{t2430.week}, Order:{t2430.order}, Subj:{t2430.subject.name}")
    except:
        print("\nTopic 2430 NOT FOUND")

if __name__ == "__main__":
    nuclear_audit()
