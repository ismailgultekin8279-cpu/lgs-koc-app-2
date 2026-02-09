from django.db import models
from students.models import Student

class ExamType(models.Model):
    NAME_CHOICES = [
        ("LGS", "LGS (Liselere Geçiş Sistemi)"),
        ("YKS_TYT", "YKS - TYT (Temel Yeterlilik)"),
        ("YKS_AYT_SAY", "YKS - AYT (Sayısal)"),
        ("YKS_AYT_EA", "YKS - AYT (Eşit Ağırlık)"),
        ("YKS_AYT_SOZ", "YKS - AYT (Sözel)"),
        ("YKS_AYT_DIL", "YKS - AYT (Dil)"),
    ]
    
    name = models.CharField(max_length=50, choices=NAME_CHOICES, unique=True)
    description = models.TextField(blank=True, default="")
    
    # Store subject weights/coefficients using a JSON field if we were using Postgres, 
    # but for SQLite/simple use, we might just define them in code or as text.
    # Let's keep it simple for now.
    
    def __str__(self):
        return self.get_name_display()

class CoachingConfig(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="coaching_config")
    
    # Target exam (Main goal)
    primary_exam = models.ForeignKey(ExamType, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Daily availability
    daily_study_seconds = models.IntegerField(default=7200) # Default 2 hours
    
    # Academic Progress Tracking
    current_academic_month = models.IntegerField(null=True, blank=True, help_text="Current focused calendar month (e.g. 9 for Sept)")
    current_academic_week = models.IntegerField(null=True, blank=True, help_text="Current focused week within the month (1-5)")
    week_started_at = models.DateField(null=True, blank=True, help_text="The date when the student started this academic week")
    
    # AI Feedback
    last_coach_message = models.TextField(blank=True, default="", help_text="Latest motivational message from AI")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Config for {self.student.full_name}"

class Subject(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            from django.utils.text import slugify
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    title = models.CharField(max_length=200)
    month = models.IntegerField(help_text="1=Ocak, ..., 9=Eylül (Takvim ayı)")
    week = models.IntegerField(help_text="Ayın kaçıncı haftası (1-5)")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['month', 'week', 'order']

    def __str__(self):
        return f"{self.subject} - {self.title}"

class StudentProgress(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='student_progress')
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'topic']

