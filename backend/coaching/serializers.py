from rest_framework import serializers
from .models import Subject, Topic, StudentProgress

class TopicSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'title', 'order', 'is_completed']

    def get_is_completed(self, obj):
        # This expects the view to prefetch 'student_progress' or we do a simple check
        # But for list views, efficient approach is needed.
        # We'll handle this by passing context or looking at annotated data.
        user = self.context.get('request').user
        if not user.is_authenticated:
            return False
            
        # Optimization: use getattr if we annotated, else query (slow for lists)
        return getattr(obj, 'is_completed', False)

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name', 'slug']

class StudentProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentProgress
        fields = ['student', 'topic', 'is_completed', 'updated_at']
