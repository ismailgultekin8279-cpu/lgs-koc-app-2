from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from students.models import Student, StudyTask
from students.serializers import StudyTaskSerializer
from .services import CoachingService
from .models import CoachingConfig
from rest_framework import serializers

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
        
        return Response({
            "weaknesses": weaknesses,
            "config": CoachingConfigSerializer(student.coaching_config).data
        })
