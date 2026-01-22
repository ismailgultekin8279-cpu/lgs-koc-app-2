import json
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from curriculum.models import CurriculumSource, Grade, Subject, Topic


class Command(BaseCommand):
    help = "Import MEB curriculum JSON into DB (Grades 6-7-8)."

    def add_arguments(self, parser):
        parser.add_argument("json_path", type=str, help="Path to meb_curriculum_YYYY_YYYY.json")

    @transaction.atomic
    def handle(self, *args, **options):
        json_path = Path(options["json_path"])
        if not json_path.exists():
            raise CommandError(f"File not found: {json_path}")

        data = json.loads(json_path.read_text(encoding="utf-8"))

        source_name = data.get("source", "MEB")
        version = data.get("version")
        if not version:
            raise CommandError("JSON must include: version (e.g. 2024-2025)")

        src, _ = CurriculumSource.objects.get_or_create(
            name=source_name,
            version=version,
            defaults={"active": True},
        )

        grades = data.get("grades", [])
        if not isinstance(grades, list) or not grades:
            raise CommandError("JSON must include: grades (non-empty list)")

        created_topics = 0

        for g in grades:
            level = g.get("grade")
            if level not in (6, 7, 8):
                raise CommandError(f"Invalid grade level: {level}. Must be 6/7/8.")

            grade_obj, _ = Grade.objects.get_or_create(level=level)

            subjects = g.get("subjects", [])
            if not isinstance(subjects, list):
                raise CommandError(f"Grade {level}: subjects must be a list")

            for s in subjects:
                subject_name = (s.get("name") or "").strip()
                if not subject_name:
                    raise CommandError(f"Grade {level}: subject name missing")

                subject_obj, _ = Subject.objects.get_or_create(
                    grade=grade_obj,
                    name=subject_name,
                )

                topics = s.get("topics", [])
                if not isinstance(topics, list):
                    raise CommandError(f"Grade {level} / {subject_name}: topics must be a list")

                for t in topics:
                    topic_name = (t.get("name") or "").strip()
                    if not topic_name:
                        raise CommandError(f"Grade {level} / {subject_name}: topic name missing")

                    order = int(t.get("order") or 0)

                    obj, created = Topic.objects.get_or_create(
                        subject=subject_obj,
                        name=topic_name,
                        defaults={"order": order},
                    )
                    if not created and obj.order != order:
                        obj.order = order
                        obj.save(update_fields=["order"])

                    if created:
                        created_topics += 1

        self.stdout.write(self.style.SUCCESS(
            f"Imported curriculum: {src.name} {src.version}. New topics: {created_topics}"
        ))
