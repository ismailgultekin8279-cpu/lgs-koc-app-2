from django.contrib import admin
from .models import CurriculumSource, Grade, Subject, Topic


@admin.register(CurriculumSource)
class CurriculumSourceAdmin(admin.ModelAdmin):
    list_display = ("name", "version", "active", "created_at")
    list_filter = ("name", "active")
    search_fields = ("name", "version")


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ("level",)
    ordering = ("level",)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ("name", "grade")
    list_filter = ("grade",)
    search_fields = ("name",)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "order")
    list_filter = ("subject__grade", "subject")
    search_fields = ("name",)
    ordering = ("subject__grade__level", "subject__name", "order")

