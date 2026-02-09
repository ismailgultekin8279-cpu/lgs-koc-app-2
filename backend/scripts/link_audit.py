
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import Student, StudyTask
from coaching.models import Topic, StudentProgress

def audit():
    student_id = 10
    print(f"--- AUDIT FOR STUDENT {student_id} ---")
    
    tasks = StudyTask.objects.filter(student_id=student_id).order_by('date', 'order')[:15]
    print("\n[RECENT TASKS]")
    for t in tasks:
        print(f"Date: {t.date} | Order: {t.order} | Status: {t.status} | Subject: {t.subject} | Topic: {t.topic_name}")
        
    progs = StudentProgress.objects.filter(student_id=student_id, is_completed=True)
    print("\n[COMPLETED PROGRESS]")
    for p in progs:
        print(f"Topic: {p.topic.subject.name} - {p.topic.title} (ID: {p.topic.id})")

    # Check for potential mismatches
    print("\n[POTENTIAL MISMATCHES - CHECKING NORMALIZATION]")
    def normalize(text):
        if not text: return ""
        text = text.lower()
        replacements = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c'}
        for old, new in replacements.items(): text = text.replace(old, new)
        return "".join(c for c in text if c.isalnum())

    pending_done = StudyTask.objects.filter(student_id=student_id, status='done')
    for t in pending_done:
        clean = t.topic_name.replace("(Pekiştirme)", "").replace("(Öğrenme)", "").strip()
        norm_t = normalize(clean)
        found = False
        # Simplified subject name for matching
        subj_map = {"İngilizce": "Yabancı Dil", "İnkılap": "T.C. İnkılap Tarihi"}
        search_subj = subj_map.get(t.subject, t.subject)
        
        matches = Topic.objects.filter(subject__name__iexact=search_subj)
        for m in matches:
            if normalize(m.title) == norm_t:
                found = True
                break
        
        if not found:
            print(f"FAILED TO MATCH: Task Topic '{t.topic_name}' (Subject: {t.subject})")

audit()
