from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from students.models import Student, ExamResult
from students.api.serializers import (
    StudentSerializer,
    ExamResultSerializer,
    ExamResultsBulkUpsertSerializer,
)


class StudentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Student.objects.all().order_by("id")
    serializer_class = StudentSerializer
    permission_classes = []


class ExamResultViewSet(viewsets.ModelViewSet):
    queryset = ExamResult.objects.all()
    serializer_class = ExamResultSerializer
    permission_classes = []

    def get_queryset(self):
        qs = super().get_queryset()

        # frontend tarafında bazen student, bazen student_id gönderiliyor olabilir
        student_id = (
            self.request.query_params.get("student_id")
            or self.request.query_params.get("student")
        )
        exam_date = self.request.query_params.get("exam_date")

        if student_id:
            qs = qs.filter(student_id=student_id)
        if exam_date:
            qs = qs.filter(exam_date=exam_date)

        return qs.order_by("-exam_date", "subject")

    @action(detail=False, methods=["post"], url_path="bulk-upsert")
    def bulk_upsert(self, request):
        serializer = ExamResultsBulkUpsertSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        student_id = data["student"]
        exam_date = data["exam_date"]
        results = data["results"]

        with transaction.atomic():
            for item in results:
                ExamResult.objects.update_or_create(
                    student_id=student_id,
                    exam_date=exam_date,
                    subject=item["subject"],
                    defaults={
                        "correct": item["correct"],
                        "wrong": item["wrong"],
                        "blank": item["blank"],
                    },
                )

        qs = ExamResult.objects.filter(student_id=student_id, exam_date=exam_date).order_by("subject")
        return Response(ExamResultSerializer(qs, many=True).data, status=status.HTTP_200_OK)
