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
    
    # Preferences
    focus_subjects = models.JSONField(default=list, blank=True) # List of subject names to focus on
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Config for {self.student.full_name}"
