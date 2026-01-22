from django.db import models


class CurriculumSource(models.Model):
    name = models.CharField(max_length=50)      # "MEB"
    version = models.CharField(max_length=20)   # "2024-2025"
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("name", "version")

    def __str__(self):
        return f"{self.name} {self.version}"


class Grade(models.Model):
    level = models.IntegerField()  # 6, 7, 8

    class Meta:
        unique_together = ("level",)

    def __str__(self):
        return f"{self.level}. Sınıf"


class Subject(models.Model):
    grade = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name="subjects")
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ("grade", "name")

    def __str__(self):
        return f"{self.name} ({self.grade.level})"


class Topic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="topics")
    name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        unique_together = ("subject", "name")
        ordering = ("subject__grade__level", "subject__name", "order", "name")

    def __str__(self):
        return f"{self.name} [{self.subject}]"
def save(self, *args, **kwargs):
    if self.active:
        CurriculumSource.objects.filter(name=self.name).exclude(pk=self.pk).update(active=False)
    super().save(*args, **kwargs)
