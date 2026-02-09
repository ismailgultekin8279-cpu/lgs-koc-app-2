from google import genai
import json
import os
from datetime import date
from django.conf import settings
from students.models import StudyTask
from .models import Subject, Topic, StudentProgress

class AICoachingService:
    def __init__(self, student):
        self.student = student
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        print(f"DEBUG: AICoachingService Init. Key Length: {len(self.api_key) if self.api_key else 'None'}")
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def get_critical_subjects(self, threshold=6.8):
        """Standardized way to get underperforming subjects."""
        weights = self._calculate_subject_weights()
        criticals = [s for s, w in weights.items() if w > threshold]
        criticals.sort(key=lambda s: weights[s], reverse=True)
        return criticals

    def get_coach_message(self):
        """Generates a smart, diversifed coach feedback message."""
        critical_subjects = self.get_critical_subjects()
        top_weakness = critical_subjects[0] if critical_subjects else None
        
        msg = "Akıllı Koç 2.0: 2 Ana + 1 Yan ders rotasyonuyla odaklanmanı artırıyoruz! Cumartesi deneme gününü sakın unutma! 🚀"
        
        if critical_subjects:
            # DIVERSITY RULE: We want to show the Top 3, 
            # BUT we want to ensure at least one 'Minor' subject is mentioned if any minor is critical.
            main_subjs = ["Matematik", "Fen Bilimleri", "Türkçe"]
            top_3 = []
            
            # 1. Add mandatory Top 1 (Absolute worst)
            top_3.append(critical_subjects[0])
            
            # 2. Add next worst
            remaining = [s for s in critical_subjects if s not in top_3]
            if remaining:
                top_3.append(remaining[0])
                
            # 3. For the 3rd spot, prefer a subject from a different 'priority group' if possible
            remaining = [s for s in critical_subjects if s not in top_3]
            if remaining:
                if all(s in main_subjs for s in top_3):
                    minor = next((s for s in remaining if s not in main_subjs), remaining[0])
                    top_3.append(minor)
                else:
                    top_3.append(remaining[0])
            
            if len(top_3) > 1:
                order_map = {s: i for i, s in enumerate(critical_subjects)}
                top_3.sort(key=lambda s: order_map[s])
                
                if len(top_3) == 3:
                    subj_list_str = f"{top_3[0]}, {top_3[1]} ve {top_3[2]}"
                else:
                    subj_list_str = " ve ".join(top_3)
                msg = f"{subj_list_str} konularında zorlandığını görüyorum. Programını senin için 'Kritik' takviye görevlerle güncelledim. Pes etmek yok! 💪🔥"
            else:
                msg = f"{top_weakness} dersinde önemli eksiklerin olduğunu tespit ettim. Programını senin için 'Kritik' takviye görevlerle güncelledim. Başaracağız! 💪🔥"
        
        return msg

    def _calculate_subject_weights(self):
        """
        Calculates dynamic weights based on LGS coefficients and recent exam results.
        Returns a dict of subject names to weight values.
        """
        from students.models import ExamResult
        
        # Base LGS Coefficients - Boosted Matematik
        weights = {
            "Matematik": 5.0,
            "Fen Bilimleri": 4.0,
            "Türkçe": 4.0,
            "T.C. İnkılap Tarihi": 2.0,
            "Yabancı Dil": 2.0,
            "Din Kültürü": 2.0
        }
        
        # Analyze last 3 exams
        # Note: We query twice to avoid sliced queryset filtering issues
        base_query = ExamResult.objects.filter(student_id=self.student.id).order_by("-exam_date", "-id")
        
        if not base_query.exists():
            return weights
            
        # 2. Individual Subject Analysis (Latest Performance)
        # We look at the most recent result for EACH subject to determine current state
        for subj_name in weights.keys():
            latest_res = base_query.filter(subject__icontains=subj_name).first()
            if not latest_res:
                continue
                
            max_q = 20 if subj_name in ["Matematik", "Fen Bilimleri", "Türkçe"] else 10
            perf = (latest_res.net / max_q) if max_q > 0 else 0.5
            
            if perf < 0.45: # CRITICAL FAIL (under 45%)
                multiplier = 1.0 + (0.6 - perf) * 2.5 
                multiplier = min(4.0, max(2.5, multiplier))
                
                # RECENCY BIAS: If this fail happened TODAY (latest exam), boost it further
                # This ensures new failures aren't drowned by historical averages
                if latest_res.exam_date == base_query.first().exam_date:
                    multiplier *= 2.0
                    
                weights[subj_name] *= multiplier
            elif perf > 0.85: # EXCELLENT (above 85%)
                # PERMANENT FORGIVENESS: Success sticks!
                weights[subj_name] *= 0.2
                weights[subj_name] = min(weights[subj_name], 4.5)

        # 3. Add impact from 3-exam Average (Long-term trend for non-improving subjects)
        recent_exams = base_query[:18]
        subj_stats = {}
        for ex in recent_exams:
            if ex.subject not in subj_stats: subj_stats[ex.subject] = []
            max_q = 20 if ex.subject in ["Matematik", "Fen Bilimleri", "Türkçe"] else 10
            perf = (ex.net / max_q) if max_q > 0 else 0.5
            subj_stats[ex.subject].append(max(0, perf))
            
        for subj, perfs in subj_stats.items():
            # Get the base key for internal weights
            weight_key = next((k for k in weights if k.lower() in subj.lower() or subj.lower() in k.lower()), None)
            if not weight_key: continue
            
            # FORGIVENESS CHECK: If LATEST for THIS subject is successful, ignore history
            latest_for_subj = base_query.filter(subject__icontains=weight_key).first()
            is_latest_success = latest_for_subj and (latest_for_subj.net / (20 if weight_key in ["Matematik", "Fen Bilimleri", "Türkçe"] else 10)) > 0.85
            
            avg_perf = sum(perfs) / len(perfs)
            if avg_perf < 0.6 and not is_latest_success:
                multiplier = 1.0 + (0.6 - avg_perf) * 1.5 
                multiplier = min(2.1, max(1.0, multiplier))
                weights[weight_key] *= multiplier
                
                # EMERGENCY PRIORITY for Matematik
                if "matematik" in weight_key.lower() and avg_perf < 0.25:
                     weights[weight_key] += 5.0
                        
        return weights

    def _get_academic_week_scope(self):
        """
        Determines the current 'Active Academic Week' for the student.
        Enforces a 7-day temporal lock on the current month/week.
        """
        from .models import CoachingConfig
        # Ensure we have a config
        config, _ = CoachingConfig.objects.get_or_create(student=self.student)
        
        month_priority = {9: 0, 10: 1, 11: 2, 12: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9}
        today = date.today()
        
        should_advance = False
        
        # 1. Check if we need to initialize or advance based on time
        if not config.current_academic_month or not config.current_academic_week or not config.week_started_at:
             should_advance = True
             print("DEBUG: First time setup (fields missing).")
        else:
            # Check if 7 days have passed since the start of this week
            days_passed = (today - config.week_started_at).days
            print(f"DEBUG: Checking Week Lock. Started: {config.week_started_at}, Today: {today}, Days Passed: {days_passed}")
            
            # Check if all topics in the current academic week are completed
            current_week_topics = Topic.objects.filter(
                month=config.current_academic_month, 
                week=config.current_academic_week
            )
            total_topics = current_week_topics.count()
            completed_in_week = StudentProgress.objects.filter(
                student=self.student,
                topic__in=current_week_topics,
                is_completed=True
            ).count()
            
            is_week_completed = (total_topics > 0 and completed_in_week == total_topics)
            print(f"DEBUG: Completion Check. Total: {total_topics}, Done: {completed_in_week}. Week Completed? {is_week_completed}")
            
            # NEW: Aggressive Sequential Progression
            # If all work is done, we advance immediately.
            if is_week_completed:
                should_advance = True
                print("DEBUG: Advance TRIGGERED (Curriculum COMPLETED).")
            elif days_passed >= 7:
                # If time is up, we also advance to keep momentum, 
                # but the generator will still pick up old incomplete topics from the academic scope.
                should_advance = True
                print("DEBUG: Advance TRIGGERED (Time Limit reached).")
            else:
                should_advance = False
        
        if should_advance:
            # Find the best target week
            # Get all topics sorted by academic order
            all_topics = list(Topic.objects.all())
            all_topics.sort(key=lambda t: (month_priority.get(t.month, 99), t.week, t.order))
            
            # Get completed topic IDs - refresh this
            completed_ids = set(StudentProgress.objects.filter(
                student=self.student,
                is_completed=True
            ).values_list('topic_id', flat=True))
            
            if config.current_academic_month and config.current_academic_week:
                # Advance logic: Find first week AFTER current week
                target_month = None
                target_week = None
                
                cur_prio = month_priority.get(config.current_academic_month, 99)
                cur_week = config.current_academic_week
                
                for t in all_topics:
                    t_prio = month_priority.get(t.month, 99)
                    if (t_prio > cur_prio) or (t_prio == cur_prio and t.week > cur_week):
                        target_month = t.month
                        target_week = t.week
                        break
                
                if target_month:
                    config.current_academic_month = target_month
                    config.current_academic_week = target_week
                    config.week_started_at = today
                    config.save()
            else:
                # First time setup: find earliest uncompleted topic's week
                target_month = None
                target_week = None
                for t in all_topics:
                    if t.id not in completed_ids:
                        target_month = t.month
                        target_week = t.week
                        break
                
                if target_month:
                    config.current_academic_month = target_month
                    config.current_academic_week = target_week
                    config.week_started_at = today
                    config.save()
        
        # Final target from config
        m = config.current_academic_month
        w = config.current_academic_week
        
        if not m:
            return None, None, []
            
        # 2. Get ALL topics for that specific month and week
        week_topics = Topic.objects.filter(month=m, week=w)
        return m, w, week_topics

    def _get_next_curriculum_topic(self, subject_name):
        # We might still need this for singleton lookups or fallback
        # but the primary logic will move to the week scope.
        try:
            subject = Subject.objects.get(name__iexact=subject_name)
        except Subject.DoesNotExist:
            return None
        
        all_topics = list(Topic.objects.filter(subject=subject))
        month_priority = {9: 0, 10: 1, 11: 2, 12: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 8, 6: 9}
        all_topics.sort(key=lambda t: (month_priority.get(t.month, 99), t.week, t.order))
        
        completed_ids = set(StudentProgress.objects.filter(
            student=self.student,
            topic__subject=subject,
            is_completed=True
        ).values_list('topic_id', flat=True))

        for topic in all_topics:
            if topic.id not in completed_ids:
                return topic
        return None

    def generate_plan(self, context, target_date):
        if not self.api_key:
            # Even without API key, we can now generate smart fallback using curriculum
            return self._generate_fallback_response(context, target_date)
            # return None

        prompt = self._build_prompt(context, target_date)
        
        try:
            # New SDK usage: client.models.generate_content
            response = self.client.models.generate_content(
                model='gemini-2.0-flash', 
                contents=prompt
            )
            
            # Access text via response.text (or correct attribute for new SDK)
            text = response.text.replace('```json', '').replace('```', '').strip()
            data = json.loads(text)
            
            return self._parse_and_save_tasks(data, target_date)
        except Exception as e:
            print(f"AI Generation Error: {e}")
            return self._generate_fallback_response(context, target_date)

    def _generate_fallback_response(self, context, target_date):
        """
        Deterministic sequential plan generation.
        Strictly follows curriculum order across all weeks.
        """
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
        # Main Subjects (Rotated)
        main_subjs = ["Matematik", "Fen Bilimleri", "Türkçe"]
        # Minor Subjects (Rotated)
        minor_subjs = ["T.C. İnkılap Tarihi", "Yabancı Dil", "Din Kültürü"]

        # 2+1 Logic: 2 Main + 1 Minor per day
        # Detect primary weakness for specific alerts
        subj_weights = self._calculate_subject_weights()
        
        # Multiple weakness detection
        # Set threshold high enough so base weights (5.0, 4.0, 2.0) DON'T trigger it
        crit_threshold = 6.8 
        critical_subjects = [s for s, w in subj_weights.items() if w > crit_threshold]
        critical_subjects.sort(key=lambda s: subj_weights[s], reverse=True)
        
        top_weakness = critical_subjects[0] if critical_subjects else None
        max_w = subj_weights[top_weakness] if top_weakness else 0
        
        print(f"DEBUG PLAN: Student {self.student.id} | Weights: {subj_weights} | Critical: {critical_subjects}")

        print(f"DEBUG PLAN: Student {self.student.id} | Weights: {subj_weights} | Critical: {critical_subjects}")

        # Use centralized messaging with diversity rule (ensures minor subjs are called out)
        msg = self.get_coach_message()

        from datetime import timedelta
        for d in range(7):
            current_dt = target_date + timedelta(days=d)
            weekday = current_dt.weekday() # 0=Monday, 5=Saturday, 6=Sunday
            daily_tasks = []
            
            # Weekend Logic
            if weekday == 5: # Saturday: Mock Exam
                daily_tasks.append({
                    "subject": "Deneme Sınavı",
                    "topic": "Haftalık LGS Provası + Yanlış Analizi",
                    "task_type": "test",
                    "question_count": 90,
                    "duration_minutes": 155
                })
            elif weekday == 6: # Sunday: Recovery
                daily_tasks.append({
                    "subject": "Genel Tekrar",
                    "topic": "Zayıf Konuların Telafisi ve Dinlenme",
                    "task_type": "review",
                    "question_count": 0,
                    "duration_minutes": 120
                })
            else:
                # Weekdays: Dynamic Selection
                # Weekdays: Balanced Rolling Rotation
                # Based on the Day of the Week (0=Mon...4=Fri) to ensure variety
                # regardless of when the student regenerates the plan.
                idx1 = weekday % 3
                idx2 = (weekday + 1) % 3
                active_main = [main_subjs[idx1], main_subjs[idx2]]
                
                # Interleave Minors
                active_minor = [minor_subjs[weekday % 3]]
                
                for subj_name in (active_main + active_minor):
                    topic_idx = next((i for i, t in enumerate(current_incomplete) if t.subject.name == subj_name), None)
                    
                    is_crit = (subj_name in critical_subjects)
                    print(f"DEBUG TASK: Subj={subj_name} | Crit={is_crit}")
                    
                    if topic_idx is not None:
                        topic = current_incomplete.pop(topic_idx)
                        display_title = f"Kritik: {topic.title}" if is_crit else topic.title
                        
                        daily_tasks.append({
                            "id": topic.id,
                            "subject": subj_name,
                            "topic": display_title,
                            "task_type": "remediation" if is_crit else "practice",
                            "question_count": 50 if is_crit else (40 if subj_name in main_subjs else 20),
                            "duration_minutes": 75 if is_crit else (60 if subj_name in main_subjs else 30)
                        })
                    else:
                        daily_tasks.append({
                            "subject": subj_name,
                            "topic": f"Kritik: {subj_name} Genel Tekrar" if is_crit else f"{subj_name} Genel Tekrar",
                            "task_type": "remediation" if is_crit else "review",
                            "question_count": 25 if is_crit else 15,
                            "duration_minutes": 45 if is_crit else 30
                        })
            
            days_data.append({"day_offset": d, "tasks": daily_tasks})
            
        return self._parse_and_save_tasks({"plan": days_data, "coach_message": msg}, target_date)

    def _build_prompt(self, context, target_date):
        # 1. Determine Current Academic Week Scope
        m, w, week_topics = self._get_academic_week_scope()
        
        # Filter incomplete topics for the prompt to guide AI away from completed work
        completed_ids = set(StudentProgress.objects.filter(
            student=self.student,
            is_completed=True
        ).values_list('topic_id', flat=True))
        
        incomplete_topics = [t for t in week_topics if t.id not in completed_ids]

        curriculum_info = []
        if m:
            week_name = {9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık", 1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"}.get(m, str(m))
            curriculum_info.append(f"CURRENT ACADEMIC TARGET: {week_name} Month, Week {w}")
            
            if not incomplete_topics:
                curriculum_info.append("ALL core topics for this week are COMPLETED. Focus on review or advanced practice.")
            else:
                # Group by subject
                from collections import defaultdict
                by_subj = defaultdict(list)
                for t in incomplete_topics:
                    by_subj[t.subject.name].append(t.title)
                
                curriculum_info.append("PENDING TOPICS for this week (Focus on these):")
                for subj, t_list in by_subj.items():
                    curriculum_info.append(f"- {subj}: {t_list}")
        else:
            curriculum_info.append("Student has completed the entire curriculum.")
        
        curr_str = "\n".join(curriculum_info)

        return f"""
        Act as an expert student coach for exam preparation (LGS in Turkey).
        Student Profile:
        - Name: {context['student_name']}
        - Grade: {context['grade']}
        - Target Score: {context['target_score']}
        - Exam Group: {context['exam_group']}
        - Weak Subjects: {', '.join(context['weak_subjects'])}
        
        Curriculum Status (CRITICAL: You MUST use the 'Current Topic' titles EXACTLY as written below for the 'topic' field in JSON):
        {curr_str}
        
        Recent Exam Results:
        {json.dumps(context['recent_exams_summary'], indent=2)}
        
        Recently Completed Tasks:
        {json.dumps(context['completed_tasks_summary'], indent=2)}

        Goal: Create a COMPREHENSIVE 7-DAY study plan starting from {target_date}.
        
        LGS Scoring Coefficients (CRITICAL):
        - Matematik: 4 points
        - Fen Bilimleri: 4 points
        - Türkçe: 4 points
        - T.C. İnkılap Tarihi: 2 points
        - Yabancı Dil: 2 points
        - Din Kültürü: 2 points
        
        Strategy (CRITICAL RULES):
        1. Daily Cycle (Monday-Friday): EXACTLY 3 TASKS PER DAY.
           - Rule: "2 Main + 1 Minor" rotation.
           - Main Subjects: Matematik, Fen Bilimleri, Türkçe.
           - Minor Subjects: T.C. İnkılap Tarihi, Yabancı Dil, Din Kültürü.
           - Mix them every day so students don't burnout but focus deeply on 3 subjects.
        2. Weekend Logic (CRITICAL):
           - Saturday: 1 Big Task for "Deneme Sınavı" (Mock Exam) and 1 Task for "Analiz" (Wrong Question Review).
           - Sunday: 1 Task for "Haftalık Telafi" (Review of weak topics from the week) and 1 Task for "Dinlenme" (Rest).
        3. Adaptive Weights:
           - Use the provided Exam Results to prioritize subjects with low performance.
           - Give more slots to subjects with failing scores.
        4. Curriculum (STRICT WEEK LOCK): 
           - You MUST ONLY use the topics provided in the "Curriculum Status" section above.
           - DO NOT pick topics from future weeks or months.
           - If a subject has very few topics for this week, you MUST REPEAT them across different days with varied task types.
        
        Dynamic Weights from Exam Analysis:
        {json.dumps(self._calculate_subject_weights(), indent=2)}
        
        Return ONLY valid JSON in this format:
        {{
            "coach_message": "A motivating message for the week, mentioning that we are focusing on mastering this week's topics.",
            "plan": [
                {{
                    "day_offset": 0 (for {target_date}), 1, 2, ..., 6,
                    "tasks": [
                        {{
                            "subject": "Matematik",
                            "topic": "Topic Name",
                            "task_type": "practice",
                            "question_count": 30,
                            "duration_minutes": 45
                        }}
                    ]
                }}
            ]
        }}
        """

    def _parse_and_save_tasks(self, data, start_date):
        # 0. Weight Analysis for Message Protection
        weights = self._calculate_subject_weights()
        crit_threshold = 4.1
        critical_subjects = [s for s, w in weights.items() if w > crit_threshold]
        critical_subjects.sort(key=lambda s: weights[s], reverse=True)

        coach_message = data.get('coach_message', '')
        
        # If we have a crisis but the message is generic or empty, force a crisis message
        is_generic = any(word in coach_message.lower() for word in ["harika", "gidiyorsun", "devam et", "rotasyonuyla", "unurma"])
        if critical_subjects and (not coach_message or is_generic):
            if len(critical_subjects) > 1:
                subj_list_str = " ve ".join(critical_subjects[:2])
                coach_message = f"{subj_list_str} konularında zorlandığını görüyorum. Programını senin için 'Kritik' takviye görevlerle güncelledim. Pes etmek yok! 💪🔥"
            else:
                top_w = critical_subjects[0]
                coach_message = f"{top_w} dersinde önemli eksiklerin olduğunu tespit ettim. Programını senin için 'Kritik' takviye görevlerle güncelledim. Başaracağız! 💪🔥"

        if coach_message:
            from .models import CoachingConfig
            config, _ = CoachingConfig.objects.get_or_create(student=self.student)
            config.last_coach_message = coach_message
            config.save()
            print(f"DEBUG SAVE: Message Saved -> {coach_message[:50]}...")
        all_created_tasks = []
        plan_days = data.get('plan', [])
        
        # If the AI returned the old format (flat tasks list)
        if not plan_days and 'tasks' in data:
            plan_days = [{"day_offset": 0, "tasks": data['tasks']}]

        from datetime import timedelta
        
        for day_data in plan_days:
            offset = day_data.get('day_offset', 0)
            target_date = start_date + timedelta(days=offset)
            
            # Clear existing for this specific day in the range
            StudyTask.objects.filter(student=self.student, date=target_date).delete()
            
            task_list = day_data.get('tasks', [])
            for idx, t_data in enumerate(task_list):
                t_id = t_data.get('id')
                t_title = t_data.get('topic', 'General Study')
                t_subject = t_data.get('subject', 'General')

                # Safety: If ID is missing, try to resolve it by title within this week's scope
                if not t_id and t_subject != 'General':
                    # Extract the base title from parenthetical garbage
                    import re
                    clean_lookup = re.sub(r'\(.*?\)', '', t_title).strip()
                    
                    # Fuzzy match within the student's current likely subject topics
                    res_topic = Topic.objects.filter(
                        subject__name__iexact=t_subject,
                        title__icontains=clean_lookup
                    ).first()
                    if res_topic:
                        t_id = res_topic.id

                all_created_tasks.append(StudyTask(
                    student=self.student,
                    date=target_date,
                    subject=t_subject,
                    topic_id=t_id, 
                    topic_name=t_title,
                    task_type=t_data.get('task_type', 'practice'),
                    question_count=t_data.get('question_count', 20),
                    recommended_seconds=t_data.get('duration_minutes', 30) * 60,
                    order=idx + 1
                ))
            
        StudyTask.objects.bulk_create(all_created_tasks)
        return all_created_tasks
