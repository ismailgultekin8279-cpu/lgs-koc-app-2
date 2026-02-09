
import os
import django
import sys
from datetime import date

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Subject, Topic, StudentProgress, CoachingConfig
from students.models import Student, StudyTask
from coaching.ai_service import AICoachingService

def auditor():
    sid = 10
    log_file = "scripts/super_audit_log.txt"
    
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"--- SUPER AUDIT FOR STUDENT {sid} ---\n")
        f.write(f"Timestamp: {date.today()}\n\n")
        
        # 1. Student Check
        try:
            student = Student.objects.get(id=sid)
            f.write(f"Student: {student.full_name} (ID: {student.id})\n")
        except Student.DoesNotExist:
            f.write("ERROR: Student 10 NOT FOUND\n")
            return

        # 2. Subject Exact Names
        f.write("\n--- SUBJECTS ---\n")
        for s in Subject.objects.all():
            f.write(f"ID: {s.id} | Name: {repr(s.name)} | Slug: {repr(s.slug)}\n")

        # 3. Active Scope
        config, _ = CoachingConfig.objects.get_or_create(student=student)
        f.write(f"\n--- CONFIG ---\n")
        f.write(f"Month: {config.current_academic_month} | Week: {config.current_academic_week} | Started: {config.week_started_at}\n")

        # 4. AICoachingService Logic Simulation
        service = AICoachingService(student)
        m, w, week_topics = service._get_academic_week_scope()
        f.write(f"Service Scope: Month {m}, Week {w}, Topics Count: {week_topics.count() if week_topics else 0}\n")
        
        math_subj = Subject.objects.filter(name="Matematik").first()
        if math_subj:
            f.write(f"Math Subject Found: ID {math_subj.id}\n")
            completed_orders = list(StudentProgress.objects.filter(
                student=student,
                topic__subject=math_subj,
                topic__month=m,
                topic__week=w,
                is_completed=True
            ).values_list('topic__order', flat=True))
            f.write(f"Completed Orders for M{m}W{w}: {completed_orders}\n")
            
            # Why is 0 missing?
            topic_0 = Topic.objects.filter(subject=math_subj, month=m, week=w, order=0).first()
            if topic_0:
                f.write(f"Topic Order 0: {topic_0.title} (ID: {topic_0.id})\n")
                prog = StudentProgress.objects.filter(student=student, topic=topic_0).first()
                if prog:
                    f.write(f"Progress Record exists: ID {prog.id} | is_completed: {prog.is_completed}\n")
                else:
                    f.write("Progress Record NOT FOUND for Topic 0\n")
            else:
                f.write("Topic Order 0 NOT FOUND in M9 W1 for Math!\n")
        else:
            f.write("ERROR: Mathematic subject NOT FOUND by name 'Matematik'\n")

        # 5. Check all topics for this week
        if week_topics:
            f.write("\n--- WEEK TOPICS ---\n")
            for t in week_topics.order_by('subject__name', 'order'):
                done = StudentProgress.objects.filter(student=student, topic=t, is_completed=True).exists()
                f.write(f"Subj: {t.subject.name:15} | Ord: {t.order} | Done: {done:5} | ID: {t.id:10} | Title: {t.title}\n")

        # 6. Check TODAY'S tasks
        today = date.today()
        todays_tasks = StudyTask.objects.filter(student=student, date=today).order_by('order')
        f.write(f"\n--- TODAY'S TASKS ({today}) ---\n")
        for t in todays_tasks:
            f.write(f"Task ID: {t.id:8} | Status: {t.status:10} | TopicID: {t.topic_id:8} | Name: {t.topic_name}\n")

    print(f"Audit complete. Results in {log_file}")

if __name__ == "__main__":
    auditor()
