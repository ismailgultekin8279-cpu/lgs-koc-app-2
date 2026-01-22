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
            
        # 1. Check if plan already exists
        if StudyTask.objects.filter(student=self.student, date=target_date).exists():
            return []

        # 2. Gather Context for AI
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
        # Try Real AI first
        from .ai_service import AICoachingService
        ai_service = AICoachingService(self.student)
        real_ai_tasks = ai_service.generate_plan(context, target_date)
        
        if real_ai_tasks:
            return real_ai_tasks
            
        # Fallback to Rule-based Proxy
        return self._generate_ai_plan_proxy(target_date, context)

    def _generate_ai_plan_proxy(self, target_date, context):
        """
        Simulates an AI decision making process.
        Ensures checking completed tasks to avoid repetition and focus on weaknesses.
        """
        tasks = []
        exam_group = context['exam_group']
        weaknesses = context['weak_subjects']
        completed_summary = context['completed_tasks_summary']
        
        # Base subjects
        if exam_group == "YKS":
             pool = ["TYT Matematik", "TYT Türkçe", "Fizik", "Kimya", "Biyoloji"]
        else:
             pool = ["Matematik", "Fen Bilimleri", "Türkçe", "İnkılap", "İngilizce"]
             
        # Logic: If student recently completed a task in a subject, deprioritize it TODAY 
        # unless it's a major weakness.
        
        recently_studied_subjects = [t.split(' - ')[0] for t in completed_summary]
        
        # Priorities: Weaknesses > Not Studied Recently > Studied Recently
        priority_queue = []
        
        # 1. Add Weaknesses (Top Priority)
        for w in weaknesses:
            priority_queue.append((w, "focus_weakness"))
            
        # 2. Add subjects not studied recently
        for p in pool:
            if p not in recently_studied_subjects and p not in weaknesses:
                priority_queue.append((p, "routine"))
                
        # 3. Add others if needed
        for p in pool:
            if p not in [x[0] for x in priority_queue]:
                 priority_queue.append((p, "review"))
                 
        # Select top 3 tasks
        selected = priority_queue[:3]
        
        for idx, (subj, mode) in enumerate(selected):
            q_count = 20
            duration = 1800
            task_type = "practice"
            
            if mode == "focus_weakness":
                q_count = 40
                duration = 3600
                task_type = "remediation"
            elif mode == "review":
                q_count = 15
                task_type = "review"
                
            tasks.append(StudyTask(
                student=self.student,
                date=target_date,
                subject=subj,
                topic_name=f"{subj} Genel Tekrar ({mode})", # In real AI, this would be specific topic
                task_type=task_type,
                question_count=q_count,
                recommended_seconds=duration,
                order=idx+1
            ))
            
        StudyTask.objects.bulk_create(tasks)
        return tasks

    def _analyze_weaknesses(self):
        """
        Returns a list of subject names where the student is underperforming.
        """
        # Look at last 5 exams
        recent_exams = ExamResult.objects.filter(
            student_id=self.student.id
        ).order_by('-exam_date')[:20] # ample buffer
        
        scores = {}
        counts = {}
        
        for exam in recent_exams:
            if exam.subject not in scores:
                scores[exam.subject] = 0
                counts[exam.subject] = 0
            
            # Simple metric: net / (correct + wrong + blank) if total > 0
            total_q = exam.correct + exam.wrong + exam.blank
            if total_q > 0:
                percent = (exam.net / total_q) * 100
                scores[exam.subject] += percent
                counts[exam.subject] += 1
                
        weak_subjects = []
        for subject, total_score in scores.items():
            avg_score = total_score / counts[subject]
            if avg_score < 70: # Threshold for "weakness"
                weak_subjects.append(subject)
                
        return weak_subjects
