from datetime import datetime
from django.core.management.base import BaseCommand

from students.models import Student
from students.services.planning.planner import generate_daily_plan


class Command(BaseCommand):
    help = "Günlük çalışma planı (StudyTask) üretir"

    def add_arguments(self, parser):
        parser.add_argument("--date", required=False, help="YYYY-MM-DD (boşsa bugün)")
        parser.add_argument("--student_id", type=int, required=False, help="Öğrenci ID")
        parser.add_argument("--all", action="store_true", help="Tüm öğrenciler için üret")
        parser.add_argument("--questions", type=int, default=80, help="Günlük toplam soru")
        parser.add_argument("--chunk", type=int, default=10, help="Görev başına soru (chunk)")
        parser.add_argument("--force", action="store_true", help="Aynı gün varsa silip yeniden üret")

    def handle(self, *args, **options):
        if options.get("date"):
            plan_date = datetime.strptime(options["date"], "%Y-%m-%d").date()
        else:
            plan_date = datetime.now().date()

        student_id = options.get("student_id")
        run_all = bool(options.get("all"))

        if not run_all and not student_id:
            self.stderr.write("HATA: --student_id veya --all vermelisin.")
            return

        if run_all:
            students = list(Student.objects.all().only("id"))
        else:
            students = [Student.objects.only("id").get(id=student_id)]

        total_tasks = 0
        total_questions = 0

        for s in students:
            result = generate_daily_plan(
                student_id=s.id,
                plan_date=plan_date,
                target_questions=options["questions"],
                chunk_size=options["chunk"],
                force=options["force"],
            )
            total_tasks += result.created_count
            total_questions += result.total_questions

        self.stdout.write(
            self.style.SUCCESS(
                f"Plan üretildi. date={plan_date}, students={len(students)}, tasks={total_tasks}, questions={total_questions}"
            )
        )
