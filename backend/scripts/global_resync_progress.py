
import os
import django
import re
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend_project.settings')
django.setup()

from students.models import StudyTask
from coaching.models import Topic, StudentProgress

def normalize(text):
    if not text: return ""
    text = text.lower()
    replacements = {'ı': 'i', 'ğ': 'g', 'ü': 'u', 'ş': 's', 'ö': 'o', 'ç': 'c'}
    for old, new in replacements.items(): text = text.replace(old, new)
    return "".join(c for c in text if c.isalnum())

def resync(student_id):
    print(f"--- RE-SYNCING PROGRESS FOR STUDENT {student_id} ---")
    done_tasks = StudyTask.objects.filter(student_id=student_id, status='done')
    
    count = 0
    for task in done_tasks:
        # Linkage logic (same as in views.py)
        clean_name = task.topic_name
        if " - " in clean_name: clean_name = clean_name.split(" - ", 1)[1]
        clean_name = re.sub(r'\(\d+\.\s*Ay,\s*\d+\.\s*Hafta\)', '', clean_name).strip()
        
        suffixes = [r'\(Öğrenme\)', r'\(Pekiştirme\)', r'\(Genel Tekrar\)', r'\(Kritik Soru Çözümü\)', r'\(Hız Testi\)', r'\(Zor Sorular\)']
        for pattern in suffixes:
            clean_name = re.sub(pattern, '', clean_name, flags=re.IGNORECASE).strip()
            
        norm_task = normalize(clean_name)
        
        subject_name = task.subject
        aliases = {"İngilizce": "Yabancı Dil", "İnkılap": "T.C. İnkılap Tarihi", "Fen": "Fen Bilimleri", "TC İnkılap": "T.C. İnkılap Tarihi", "Din": "Din Kültürü"}
        subject_name = aliases.get(subject_name, subject_name)

        topic = Topic.objects.filter(subject__name__iexact=subject_name).filter(title__icontains=clean_name[:10]).first()
        # Fallback to normalization if basic filter fails
        if not topic:
            for t in Topic.objects.filter(subject__name__iexact=subject_name):
                if normalize(t.title) == norm_task:
                    topic = t
                    break

        if topic:
            StudentProgress.objects.update_or_create(
                student_id=student_id,
                topic=topic,
                defaults={'is_completed': True, 'completed_at': timezone.now()}
            )
            count += 1
            
    print(f"Successfully re-synced {count} topics.")

resync(10)
