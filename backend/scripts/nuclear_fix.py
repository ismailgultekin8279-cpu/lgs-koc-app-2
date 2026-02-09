
import os
import django
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress

def nuclear_fix():
    sid = 10
    student = Student.objects.get(id=sid)
    config = student.coaching_config
    m = config.current_academic_month
    w = config.current_academic_week
    
    print(f"--- NUCLEAR FIX FOR STUDENT {sid} (Month {m}, Week {w}) ---")
    
    # 1. Get ALL completed progress for this student ever
    all_completed = StudentProgress.objects.filter(student=student, is_completed=True).select_related('topic')
    
    completed_titles = {} # (subject_id, title) -> latest completed_at
    for p in all_completed:
        key = (p.topic.subject_id, p.topic.title)
        if key not in completed_titles or (p.completed_at and p.completed_at > completed_titles[key]):
            completed_titles[key] = p.completed_at or timezone.now()

    # 2. For every title that is 'completed', ensure it's marked as completed in the ACTIVE week topics
    for (subj_id, title), dt in completed_titles.items():
        active_topic = Topic.objects.filter(subject_id=subj_id, month=m, week=w, title=title).first()
        if active_topic:
            print(f"FORCING GREEN: '{title}' in M:{m} W:{w} (ID: {active_topic.id})")
            StudentProgress.objects.update_or_create(
                student=student,
                topic=active_topic,
                defaults={'is_completed': True, 'completed_at': dt}
            )

    # 3. Also check for tasks that are 'done' and force their titles to be green in the active week
    done_tasks = StudyTask.objects.filter(student=student, status='done')
    for t in done_tasks:
        # Match by title for the active month/week
        # We need to find the subject first
        from coaching.models import Subject
        # Normalize subject (Din -> Din Kültürü etc)
        subj_name = t.subject
        aliases = {"Din": "Din Kültürü", "İngilizce": "Yabancı Dil", "İnkılap": "T.C. İnkılap Tarihi", "Fen": "Fen Bilimleri"}
        subj_name = aliases.get(subj_name, subj_name)
        
        active_topic = Topic.objects.filter(subject__name__iexact=subj_name, month=m, week=w, title=t.topic_name).first()
        if not active_topic:
            # Try cleaning parentheticals
            import re
            clean_t = re.sub(r'\(.*?\)', '', t.topic_name).strip()
            active_topic = Topic.objects.filter(subject__name__iexact=subj_name, month=m, week=w, title=clean_t).first()

        if active_topic:
            print(f"FORCING GREEN FROM TASK: '{t.topic_name}' -> '{active_topic.title}'")
            StudentProgress.objects.update_or_create(
                student=student,
                topic=active_topic,
                defaults={'is_completed': True, 'completed_at': t.completed_at or timezone.now()}
            )

    print("--- NUCLEAR FIX COMPLETE ---")

if __name__ == "__main__":
    nuclear_fix()
