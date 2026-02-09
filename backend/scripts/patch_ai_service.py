
import os

FILE_PATH = r'c:\Users\USER\Desktop\ismail proje\lgs_dershane\backend\coaching\ai_service.py'

NEW_FUNC = """    def _generate_fallback_response(self, context, target_date):
        \"\"\"
        Deterministic sequential plan generation.
        Strictly follows curriculum order across all weeks.
        \"\"\"
        # 1. Subject Check & Scope
        m, w, week_topics = self._get_academic_week_scope()
        
        # Get ALL incomplete topics for the student across the entire curriculum
        from .models import Topic, StudentProgress
        all_topics = list(Topic.objects.all().select_related('subject'))
        
        # Sort by month_priority, week, and order
        month_priority = {9: 0, 10: 1, 11: 2, 12: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9}
        all_topics.sort(key=lambda t: (month_priority.get(t.month, 99), t.week, t.order))
        
        completed_ids = set(StudentProgress.objects.filter(
            student=self.student,
            is_completed=True
        ).values_list('topic_id', flat=True))
        
        # Pool of all future work
        current_incomplete = [t for t in all_topics if t.id not in completed_ids]
        
        days_data = []
        subjects_order = ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "Yabancı Dil", "Din Kültürü"]

        for d in range(7):
            daily_tasks = []
            
            for subj_name in subjects_order:
                # Find the first available incomplete topic for this subject (Globally!)
                topic_idx = next((i for i, t in enumerate(current_incomplete) if t.subject.name == subj_name), None)
                
                if topic_idx is not None:
                    topic = current_incomplete.pop(topic_idx)
                    is_focus = (subj_name == subjects_order[d % len(subjects_order)])
                    
                    # Prefix topic name if it's outside the current week
                    is_outside = (topic.month != m or topic.week != w)
                    display_title = topic.title
                    if is_outside:
                        display_title = f"{display_title} (Önden İlerleme)"
                    elif not is_focus:
                        display_title = f"{display_title} (Pekiştirme)"
                    
                    daily_tasks.append({
                        "id": topic.id,
                        "subject": subj_name,
                        "topic": display_title,
                        "task_type": "practice" if is_focus else "review",
                        "question_count": 30 if is_focus else 15,
                        "duration_minutes": 45 if is_focus else 30
                    })
                else:
                    # True fallback if NO topics left at all in the whole year
                    daily_tasks.append({
                        "subject": subj_name,
                        "topic": f"{subj_name} Genel Tekrar",
                        "task_type": "review",
                        "question_count": 15,
                        "duration_minutes": 30
                    })
            
            days_data.append({"day_offset": d, "tasks": daily_tasks})
            
        return self._parse_and_save_tasks({"plan": days_data, "coach_message": "Akıllı Koç müfredatı senin için optimize etti! Başlayalım! 🚀"}, target_date)
"""

def patch():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    start_line = -1
    end_line = -1
    
    for i, line in enumerate(lines):
        if 'def _generate_fallback_response' in line:
            start_line = i
        if start_line != -1 and 'def _build_prompt' in line:
            end_line = i
            break
            
    if start_line != -1 and end_line != -1:
        new_lines = lines[:start_line] + [NEW_FUNC + '\n'] + lines[end_line:]
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print("Successfully patched AICoachingService.py")
    else:
        print(f"Failed to find boundaries: start={start_line}, end={end_line}")

if __name__ == "__main__":
    patch()
