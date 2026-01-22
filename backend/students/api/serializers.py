from rest_framework import serializers
from students.models import Student, ExamResult


class StudentSerializer(serializers.ModelSerializer):
    display_name = serializers.CharField(source="full_name", read_only=True)

    class Meta:
        model = Student
        fields = ["id", "display_name", "grade", "target_score"]


class ExamResultSerializer(serializers.ModelSerializer):
    net = serializers.SerializerMethodField()

    class Meta:
        model = ExamResult
        fields = [
            "id",
            "student_id",
            "exam_date",
            "subject",
            "correct",
            "wrong",
            "blank",
            "net",
            "created_at",
        ]
        read_only_fields = ["id", "net", "created_at"]

    def get_net(self, obj: ExamResult):
        return round(obj.net(), 3)


class ExamResultItemSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=64)
    correct = serializers.IntegerField(min_value=0)
    wrong = serializers.IntegerField(min_value=0)
    blank = serializers.IntegerField(min_value=0)


class ExamResultsBulkUpsertSerializer(serializers.Serializer):
    student = serializers.IntegerField()
    exam_date = serializers.DateField()
    results = ExamResultItemSerializer(many=True)
