from datetime import date, timedelta
from django.db.models import Sum, Avg
from students.models import Student, StudyTask, TopicPerformance, ExamResult
from .models import CoachingConfig, ExamType

class CoachingService:
    def __init__(self, student: Student):
        self.student = student
        self.config, _ = CoachingConfig.objects.get_or_create(student=student)

    def generate_daily_plan(self, target_date=None):
        """
        Generates StudyTasks using AI analysis of student's performance and recent completions.
        """
        if target_date is None:
            target_date = date.today()
            
        # 1. Gather Context for AI
        weak_subjects = self._analyze_weaknesses()
        recent_exams = ExamResult.objects.filter(student_id=self.student.id).order_by('-exam_date')[:3]
        
        # New Context: Completed Tasks (Last 3 days)
        last_3_days = target_date - timedelta(days=3)
        completed_tasks = StudyTask.objects.filter(
            student=self.student, 
            status='done',
            completed_at__gte=last_3_days
        ).order_by('-completed_at')

        context = {
            "student_name": self.student.full_name,
            "grade": self.student.grade,
            "target_score": self.student.target_score,
            "exam_group": self.student.exam_group,
            "weak_subjects": weak_subjects,
            "recent_exams_summary": [
                f"{e.exam_date}: {e.subject} ({e.net} net)" for e in recent_exams
            ],
            "completed_tasks_summary": [
                f"{t.subject} - {t.topic_name} ({t.question_count} qs)" for t in completed_tasks
            ]
        }
        
        # 3. Call AI
        # Bypass Real AI to ensure consistent task generation with our fixed proxy logic
        # 3. Call AI
        # Bypass Real AI to ensure consistent task generation with our fixed proxy logic
        from .ai_service import AICoachingService
        ai_service = AICoachingService(self.student)
        
        real_ai_tasks = ai_service.generate_plan(context, target_date)
        
        if real_ai_tasks:
             return real_ai_tasks
             
        # Emergency Fallback 
        return ai_service._generate_fallback_response(context, target_date)

    def _generate_ai_plan_proxy(self, target_date, context):
        """
        Simulates an AI decision making process.
        Ensures checking completed tasks to avoid repetition and focus on weaknesses.
        """
        tasks = []
        exam_group = context['exam_group']
        weaknesses = context['weak_subjects'] # This is now a unique list
        completed_summary = context['completed_tasks_summary']
        
        # Base subjects
        if exam_group == "YKS":
             pool = ["TYT Matematik", "TYT Türkçe", "Fizik", "Kimya", "Biyoloji"]
        else:
             pool = ["Matematik", "Fen Bilimleri", "Türkçe", "T.C. İnkılap Tarihi", "Din Kültürü", "Yabancı Dil"]
             
        recently_studied_subjects = [t.split(' - ')[0] for t in completed_summary]
        
        # Priority Queue Construction
        priority_queue = []
        seen_subjects = set()
        
        # 1. Add ALL Weaknesses (Top Priority)
        for w in weaknesses:
            if w not in seen_subjects:
                priority_queue.append((w, "focus_weakness"))
                seen_subjects.add(w)
            
        # 2. Add subjects not studied recently
        # We want to fill up to at least 3-4 tasks.
        # If we have many weaknesses (e.g. 3), we add them all. Then maybe add 1 routine.
        
        for p in pool:
            if p not in seen_subjects and p not in recently_studied_subjects:
                priority_queue.append((p, "routine"))
                seen_subjects.add(p)
                    
        # 3. Add others (review) if we still have very few tasks
        if len(priority_queue) < 3:
            for p in pool:
                if p not in seen_subjects:
                     priority_queue.append((p, "review"))
                     seen_subjects.add(p)
                 
        # Selection Logic
        # If we have weaknesses, show ALL of them.
        # Plus fill up to 3 tasks minima with routine tasks.
        
        final_selection = []
        weakness_count = len(weaknesses)
        
        # Selection Logic
        # If we have weaknesses, show ALL of them, NO LIMIT.
        
        final_selection = []
        
        # First, add ALL weaknesses
        for item in priority_queue:
            subj, mode = item
            if mode == "focus_weakness":
                final_selection.append(item)
                
        # Then, fill with routine/review up to a TOTAL of 6 (or more if user wants)
        # But ensure we don't duplicate logic. Ideally priority_queue is unique.
        
        current_count = len(final_selection)
        target_total = 3 # STRICT 2+1 FOR EXPERT REVIEW
        
        for item in priority_queue:
            subj, mode = item
            if mode == "focus_weakness":
                continue # Already handled in specialized logic if needed, but here we fill
            
            if len(final_selection) < target_total:
                final_selection.append(item)
            else:
                break
        
        for idx, (subj, mode) in enumerate(final_selection):
            q_count = 20
            duration = 1800
            task_type = "practice"
            
            if mode == "focus_weakness":
                q_count = 40
                duration = 3600
                task_type = "remediation"
                topic_label = "Kritik Eksik Tamamlama"
            elif mode == "review":
                q_count = 15
                task_type = "review"
                topic_label = "Genel Tekrar"
            else:
                # routine
                topic_label = "Günlük Rutin Tekrar"
                
            tasks.append(StudyTask(
                student=self.student,
                date=target_date,
                subject=subj,
                topic_name=f"{subj} - {topic_label}",
                task_type=task_type,
                question_count=q_count,
                recommended_seconds=duration,
                order=idx+1
            ))
            
        StudyTask.objects.bulk_create(tasks)
        return tasks

    def _analyze_weaknesses(self):
        """
        Delegates to AICoachingService for standardized intelligence.
        """
        from .ai_service import AICoachingService
        ai_svc = AICoachingService(self.student)
        return ai_svc.get_critical_subjects()
