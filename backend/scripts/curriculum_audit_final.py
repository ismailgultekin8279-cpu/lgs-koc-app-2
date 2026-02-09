
import os
import django
import sys
from collections import defaultdict

sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from coaching.models import Topic, StudentProgress, CoachingConfig
from students.models import Student

def audit():
    output = []
    output.append("=== CURRICULUM DATA AUDIT ===")
    
    # 1. Subject Check
    subjects = ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "Yabancı Dil", "Din Kültürü"]
    
    for m in [9, 10]:
        output.append(f"\n--- Month {m} ---")
        for w in [1, 2, 3, 4]:
            output.append(f"  Week {w}:")
            for subj in subjects:
                topics = Topic.objects.filter(month=m, week=w, subject__name=subj).order_by('order')
                titles = [t.title for t in topics]
                count = len(titles)
                output.append(f"    {subj}: {count} topics - {titles[:2]} ...")

    # 2. Student 10 State
    s = Student.objects.get(id=10)
    config = s.coaching_config
    output.append(f"\n=== STUDENT 10 STATE ===")
    output.append(f"Config: Month {config.current_academic_month}, Week {config.current_academic_week}, Started: {config.week_started_at}")
    
    # Check completed topics in Month 9 Week 1
    done_m9w1 = StudentProgress.objects.filter(student=s, topic__month=9, topic__week=1, is_completed=True)
    output.append(f"Month 9 Week 1 Completions: {done_m9w1.count()}")
    for d in done_m9w1:
        output.append(f"  [DONE] {d.topic.subject.name}: {d.topic.title}")
    
    with open('curriculum_audit_report.txt', 'w', encoding='utf-8') as f:
        f.write("\n".join(output))
    print("Audit report written to curriculum_audit_report.txt")

if __name__ == "__main__":
    audit()
