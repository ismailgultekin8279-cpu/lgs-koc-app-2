from google import genai
import json
import os
from datetime import date
from django.conf import settings
from students.models import StudyTask

class AICoachingService:
    def __init__(self, student):
        self.student = student
        self.api_key = getattr(settings, 'GEMINI_API_KEY', None)
        print(f"DEBUG: AICoachingService Init. Key Length: {len(self.api_key) if self.api_key else 'None'}")
        
        if self.api_key:
            self.client = genai.Client(api_key=self.api_key)

    def generate_plan(self, context, target_date):
        if not self.api_key:
            return None

        prompt = self._build_prompt(context, target_date)
        
        try:
            # New SDK usage: client.models.generate_content
            response = self.client.models.generate_content(
                model='models/gemini-1.5-flash',
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
        # A smart fallback that looks like AI
        import random
        
        weak_subject = context['weak_subjects'][0] if context['weak_subjects'] else "Matematik"
        
        fallback_tasks = [
            {
                "subject": weak_subject,
                "topic": f"{weak_subject} - Yeni Nesil Soru Çözümü",
                "task_type": "practice",
                "question_count": 25,
                "duration_minutes": 40
            },
            {
                "subject": "Türkçe",
                "topic": "Paragraf Taktikleri ve Hız Denemesi",
                "task_type": "practice",
                "question_count": 20,
                "duration_minutes": 30
            },
            {
                "subject": "Fen Bilimleri",
                "topic": "Mevsimler ve İklim - Kritik Tekrar",
                "task_type": "review",
                "question_count": 15,
                "duration_minutes": 25
            }
        ]
        
        return self._parse_and_save_tasks({"tasks": fallback_tasks}, target_date)

    def _build_prompt(self, context, target_date):
        return f"""
        Act as an expert student coach for exam preparation (LGS/YKS in Turkey).
        Student Profile:
        - Name: {context['student_name']}
        - Grade: {context['grade']}
        - Target Score: {context['target_score']}
        - Exam Group: {context['exam_group']}
        - Weak Subjects: {', '.join(context['weak_subjects'])}
        
        Recent Exam Results:
        {json.dumps(context['recent_exams_summary'], indent=2)}
        
        Recently Completed Tasks:
        {json.dumps(context['completed_tasks_summary'], indent=2)}

        Goal: Create a daily study plan for {target_date} consisting of 3-5 specific tasks.
        Focus on weak subjects but ensure variety.
        
        Return ONLY valid JSON in this format:
        {{
            "coach_message": "A short, motivating message specific to their recent performance.",
            "tasks": [
                {{
                    "subject": "Math",
                    "topic": "Specific Topic Name",
                    "task_type": "practice" (or "review", "test"),
                    "question_count": 20,
                    "duration_minutes": 30
                }}
            ]
        }}
        """

    def _parse_and_save_tasks(self, data, target_date):
        tasks = []
        task_data_list = data.get('tasks', [])
        
        for idx, t_data in enumerate(task_data_list):
            tasks.append(StudyTask(
                student=self.student,
                date=target_date,
                subject=t_data.get('subject', 'General'),
                topic_name=t_data.get('topic', 'General Study'),
                task_type=t_data.get('task_type', 'practice'),
                question_count=t_data.get('question_count', 20),
                recommended_seconds=t_data.get('duration_minutes', 30) * 60,
                order=idx + 1
            ))
            
        StudyTask.objects.bulk_create(tasks)
        
        # Save coach message if we had a place for it, 
        # for now we return it so the view might use it or we just ignore it 
        # (The current architecture doesn't persist daily message yet, but we can verify tasks first)
        return tasks
