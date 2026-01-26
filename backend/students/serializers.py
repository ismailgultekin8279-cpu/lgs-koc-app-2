from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Student, StudyTask, ExamResult, TopicPerformance

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(required=True)
    grade = serializers.IntegerField(required=True)
    target_score = serializers.FloatField(required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'full_name', 'grade', 'target_score')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        
        g = validated_data.get('grade')
        group = "YKS" if g and g >= 9 else "LGS"
        
        Student.objects.create(
            user=user,
            full_name=validated_data.get('full_name'),
            grade=g,
            target_score=validated_data.get('target_score', 400),
            exam_group=group
        )
        
        return user

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

class StudyTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyTask
        fields = '__all__'

class ExamResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExamResult
        fields = '__all__'

class ExamResultItemSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=64)
    correct = serializers.IntegerField(min_value=0)
    wrong = serializers.IntegerField(min_value=0)
    blank = serializers.IntegerField(min_value=0)

class ExamResultsBulkUpsertSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    exam_date = serializers.DateField()
    results = ExamResultItemSerializer(many=True)
