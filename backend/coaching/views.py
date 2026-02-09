from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from students.models import Student, StudyTask
from students.serializers import StudyTaskSerializer
from .services import CoachingService
from .models import CoachingConfig
from rest_framework import serializers
from django.db.models import Prefetch, Exists, OuterRef, F
from .models import Subject, Topic, StudentProgress
from .serializers import SubjectSerializer, TopicSerializer
from django.utils import timezone

class CoachingConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoachingConfig
        fields = '__all__'

class CoachingViewSet(viewsets.GenericViewSet):
    queryset = Student.objects.all()
    
    @action(detail=True, methods=['post'])
    def generate_plan(self, request, pk=None):
        student = self.get_object()
        service = CoachingService(student)
        
        # Optional: Allow date param
        tasks = service.generate_daily_plan()
        
        serializer = StudyTaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        Returns high-level status (weaknesses, current target, etc.)
        """
        student = self.get_object()
        service = CoachingService(student)
        weaknesses = service._analyze_weaknesses()
        
        # Simple dynamic message logic
        # 1. Check for AI Message from Config
        ai_msg = student.coaching_config.last_coach_message
        
        # 2. Unified Crisis Awareness (PROTECTION)
        from .ai_service import AICoachingService
        ai_svc = AICoachingService(student)
        weights = ai_svc._calculate_subject_weights()
        critical_subjects = ai_svc.get_critical_subjects()

        is_generic = any(word in (ai_msg or "").lower() for word in ["harika", "gidiyorsun", "devam et", "rotasyonuyla", "unurma", "durumda değil", "odaklanalım"])
        
        if critical_subjects and (not ai_msg or is_generic):
            # Dynamic Crisis Message (Real-time)
            msg = ai_svc.get_coach_message()
        elif ai_msg:
            msg = ai_msg
        elif not weaknesses:
            msg = "Harika gidiyorsun! Hiçbir eksiğin görünmüyor. Rutin tekrarlara devam et."
        else:
            top_weakness = weaknesses[0]
            if len(weaknesses) > 1:
                msg = f"{top_weakness} ve {weaknesses[1]} derslerinde eksiklerin var. Bugün bunlara odaklanalım."
            else:
                msg = f"{top_weakness} dersinde biraz eksiğin var. Bugün bu konuyu halledelim."
        
        # Add current focus info
        # ... rest remains SAME ...
        config = student.coaching_config
        current_focus = None
        if config.current_academic_month and config.current_academic_week:
            month_name = {9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık", 1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"}.get(config.current_academic_month, str(config.current_academic_month))
            current_focus = f"{month_name} {config.current_academic_week}. Hafta"

        return Response({
            "weaknesses": weaknesses,
            "weights": weights,  # Include weights for frontend transparency
            "config": CoachingConfigSerializer(student.coaching_config).data,
            "message": msg,
            "current_focus": current_focus
        })

from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Prefetch, Exists, OuterRef, F
from .models import Subject, Topic, StudentProgress
from .serializers import SubjectSerializer, TopicSerializer, StudentProgressSerializer

class CurriculumViewSet(viewsets.ModelViewSet):
    """
    A ViewSet for listing curriculum and managing progress.
    Now supports CRUD for Topics/Subjects via standard ModelViewSet methods.
    """
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
    # Enable permissions to ensure request.user is populated
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        # Override list to return the Tree structure if 'tree' param is present
        # Otherwise return standard list for Admin table
        if request.query_params.get('format') == 'tree' or request.query_params.get('view') == 'tree':
            return self.list_tree(request)
        
        return super().list(request)

    def list_tree(self, request):
        """
        Return the full curriculum tree for a specific subject (default: Matematik).

        Structure:
        {
          "subject": "Matematik",
          "months": [
             { "id": 9, "name": "Eylül", "weeks": [ ... ] }
          ]
        }
        """
        subject_slug = request.query_params.get('subject', 'matematik') # Default to math
        try:
            subject = Subject.objects.get(slug=subject_slug)
        except Subject.DoesNotExist:
            # Fallback or create default if not exists for demo
            subject, _ = Subject.objects.get_or_create(name="Matematik", slug="matematik")

        # Get student
        student = getattr(request.user, 'student_profile', None)

        # Annotate topics with is_completed
        topics = Topic.objects.filter(subject=subject).order_by('month', 'week', 'order')
        
        if student:
            # Robust Strategy: Fetch all completed IDs into a set
            completed_topic_ids = set(
                StudentProgress.objects.filter(
                    student=student, 
                    is_completed=True
                ).values_list('topic_id', flat=True)
            )
        else:
            completed_topic_ids = set()

        # Build tree manually for the frontend format
        # This is more efficient than nested serializers for this specific custom view
        months_map = {}
        month_names = {
            9: "Eylül", 10: "Ekim", 11: "Kasım", 12: "Aralık", 
            1: "Ocak", 2: "Şubat", 3: "Mart", 4: "Nisan", 5: "Mayıs", 6: "Haziran"
        }

        for topic in topics:
            m_id = topic.month
            w_id = topic.week
            
            if m_id not in months_map:
                months_map[m_id] = {
                    "id": m_id,
                    "name": month_names.get(m_id, f"{m_id}. Ay"),
                    "weeks": {}
                }
            
            if w_id not in months_map[m_id]["weeks"]:
                months_map[m_id]["weeks"][w_id] = {
                    "week_number": w_id,
                    "focus": topic.title.split(" - ")[0] if " - " in topic.title else "Konu", # Simple heuristic
                    "topics": []
                }
            
            # Add topic
            status_val = "completed" if topic.id in completed_topic_ids else "pending"
            # print(f"DEBUG API: Topic {topic.title} -> {status_val}") # Uncomment if desperate
            
            months_map[m_id]["weeks"][w_id]["topics"].append({
                "id": topic.id,
                "title": topic.title,
                "status": status_val
            })

        # Convert simple dicts to lists
        result_months = []
        # Custom academic order: Sep(9) -> Jun(6)
        academic_order = [9, 10, 11, 12, 1, 2, 3, 4, 5, 6]
        
        for m_id in academic_order:
            if m_id in months_map:
                month = months_map[m_id]
                month["weeks"] = list(month["weeks"].values())
                result_months.append(month)

        return Response({
            "subject": subject.name,
            "debug_student_id": student.id if student else "NONE",
            "months": result_months
        })

    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        """
        Toggle the completion status of a topic for the current student.
        """
        student = getattr(request.user, 'student_profile', None)
        if not student:
            print("DEBUG: Student profile not found for user.")
            return Response({"error": "Student profile not found"}, status=400)

        try:
            topic = Topic.objects.get(pk=pk)
        except Topic.DoesNotExist:
            return Response({"error": "Topic not found"}, status=404)
        
        progress, created = StudentProgress.objects.get_or_create(
            student=student,
            topic=topic
        )
        
        if request.data.get('status') == 'completed':
            progress.is_completed = True
        elif request.data.get('status') == 'pending':
            progress.is_completed = False
        else:
            # Toggle if no status provided
            progress.is_completed = not progress.is_completed
            
        if progress.is_completed:
            progress.completed_at = timezone.now()
        else:
            progress.completed_at = None
            
        progress.save()
        
        return Response({
            "id": topic.id,
            "status": "completed" if progress.is_completed else "pending"
        })
