from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="student_profile", null=True, blank=True)
    full_name = models.CharField(max_length=200)
    grade = models.IntegerField()
    target_score = models.FloatField(null=True, blank=True)
    
    # "LGS", "YKS", "ARA_SINIF" etc.
    exam_group = models.CharField(max_length=20, default="LGS", blank=True)

    @property
    def display_name(self):
        return self.full_name
        
    @property
    def name(self):
        return self.full_name

    def __str__(self):
        return f"{self.id} - {self.full_name}"


class Session(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="sessions")
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.IntegerField(default=0, null=True, blank=True)
    
    def __str__(self):
         return f"Session {self.id} - {self.student.full_name}"

class BehaviorLog(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE, related_name="logs")
    risk_level = models.IntegerField(default=0)
    note = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.id} - Risk {self.risk_level}"

class StudyTask(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("done", "Done"),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="tasks")
    date = models.DateField(db_index=True)

    # Plan ekranı için kolay alanlar
    subject = models.CharField(max_length=64, blank=True, default="")
    topic_id = models.IntegerField(null=True, blank=True)
    topic_name = models.CharField(max_length=255, blank=True, default="")

    task_type = models.CharField(max_length=32, default="practice")  # practice / repeat / test vs.
    question_count = models.IntegerField(default=0)
    recommended_seconds = models.IntegerField(default=0)

    order = models.IntegerField(default=1)

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default="pending")
    completed_at = models.DateTimeField(null=True, blank=True)
    actual_seconds = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["student", "date"]),
        ]
        ordering = ["date", "order", "id"]

    def mark_done(self):
        self.status = "done"
        self.completed_at = timezone.now()
        self.save(update_fields=["status", "completed_at"])

    def __str__(self):
        return f"{self.student_id} {self.date} {self.subject or self.topic_name or 'Task'}"


class TopicPerformance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="topic_performances")
    topic = models.IntegerField()  # Basit tutuyoruz; senin projede Topic modeli varsa sonra FK yaparız.

    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    blank = models.IntegerField(default=0)

    last_practiced_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("student", "topic")

    def __str__(self):
        return f"{self.student_id} topic={self.topic}"


class ExamResult(models.Model):
    # Student FK kullanmıyoruz; daha önce sisteminde student_id ile gidiyordun.
    student_id = models.IntegerField(db_index=True)
    exam_date = models.DateField(db_index=True)

    subject = models.CharField(max_length=64)
    subject_label = models.CharField(max_length=64, blank=True, default="")

    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    blank = models.IntegerField(default=0)
    net = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student_id", "exam_date", "subject")
        ordering = ["-exam_date", "subject"]

    def save(self, *args, **kwargs):
        if not self.subject_label:
            self.subject_label = self.subject
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} {self.exam_date} {self.subject}"
