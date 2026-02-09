
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, CoachingConfig
from students.models import Student, StudyTask

def deep_audit():
    student_id = 10
    student = Student.objects.get(id=student_id)
    print(f"=== DEEP AUDIT FOR STUDENT {student_id} ===")
    
    # 1. Subject Check
    from coaching.models import Subject
    subjects = Subject.objects.all()
    print("\nSubjects:")
    for s in subjects:
        print(f"  {s.id}: {s.name}")
        
    # 2. Topic Duplication Check
    from django.db.models import Count
    dupes = Topic.objects.values('title', 'subject', 'month', 'week').annotate(count=Count('id')).filter(count__gt=1)
    if dupes:
        print("\nDUPLICATE TOPICS FOUND:")
        for d in dupes:
            print(f"  Title: {d['title']} | Count: {d['count']}")
    else:
        print("\nNo duplicate topics (by title/subj/month/week).")
        
    # 3. StudentProgress Validity
    print("\nStudentProgress Records:")
    progs = StudentProgress.objects.filter(student=student).select_related('topic')
    for p in progs:
        print(f"  P_ID:{p.id} | T_ID:{p.topic.id} | Subj:{p.topic.subject.name} | Done:{p.is_completed} | Title:{p.topic.title}")
        
    # 4. StudyTask Frontier
    math_tasks = StudyTask.objects.filter(student=student, subject='Matematik').order_by('date', 'id')
    print("\nMath StudyTasks History:")
    for t in math_tasks:
        print(f"  TaskID:{t.id} | Date:{t.date} | TopicID:{t.topic_id} | Status:{t.status} | Title:{t.topic_name}")

if __name__ == "__main__":
    deep_audit()
