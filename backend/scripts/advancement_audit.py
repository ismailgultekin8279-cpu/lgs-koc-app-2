
import os
import django
import sys
from datetime import date

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, CoachingConfig
from students.models import Student, StudyTask

def detailed_audit():
    student_id = 10
    student = Student.objects.get(id=student_id)
    config = student.coaching_config
    m, w = config.current_academic_month, config.current_academic_week
    
    with open('diagnostic_output.txt', 'w', encoding='utf-8') as f:
        f.write(f"=== DETAILED AUDIT FOR STUDENT {student_id} ===\n")
        f.write(f"CURRENT CONFIG: Month {m}, Week {w}\n\n")
        
        # 1. Check topics for the current week
        week_topics = Topic.objects.filter(month=m, week=w).select_related('subject')
        f.write(f"Topics in Week {m}W{w}: {week_topics.count()}\n")
        
        done_ids = StudentProgress.objects.filter(
            student=student, 
            topic__month=m, 
            topic__week=w, 
            is_completed=True
        ).values_list('topic_id', flat=True)
        
        f.write(f"Completed in Week: {len(done_ids)}\n")
        
        pending = week_topics.exclude(id__in=done_ids)
        if pending.exists():
            f.write("\nSTILL PENDING IN THIS WEEK:\n")
            for t in pending:
                f.write(f"  - [{t.subject.name}] ID:{t.id} Order:{t.order} Title:{t.title}\n")
        else:
            f.write("\nALL TOPICS IN THIS WEEK ARE COMPLETED.\n")
            
        # 2. Check Advancement Logic
        month_priority = {9: 0, 10: 1, 11: 2, 12: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9}
        all_topics = list(Topic.objects.all())
        all_topics.sort(key=lambda t: (month_priority.get(t.month, 99), t.week, t.order))
        
        cur_prio = month_priority.get(m, 99)
        next_week = None
        for t in all_topics:
            t_prio = month_priority.get(t.month, 99)
            if (t_prio > cur_prio) or (t_prio == cur_prio and t.week > w):
                next_week = (t.month, t.week)
                break
        
        f.write(f"\nPotential Next Week: {next_week}\n")
        
        # 3. Check Today's Tasks
        today = date.today()
        daily_tasks = StudyTask.objects.filter(student=student, date=today).order_by('id')
        f.write(f"\nTASKS FOR TODAY ({today}):\n")
        for t in daily_tasks:
            f.write(f"  ID:{t.id} | TopicID:{t.topic_id} | Subj:{t.subject} | Status:{t.status} | Title:{t.topic_name}\n")

if __name__ == "__main__":
    detailed_audit()
